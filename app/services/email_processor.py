import json
import logging
import re
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

from app.api.schemas import ProcessEmailResponse
from app.services.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from app.utils.config import Settings
from app.utils.exceptions import AIResponseError

logger = logging.getLogger(__name__)


class EmailProcessorService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
        )

    def classify_and_reply(self, email_text: str) -> ProcessEmailResponse:
        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                temperature=0.1,
                input=[
                    {
                        "role": "system",
                        "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
                    },
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": build_user_prompt(email_text)}],
                    },
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "email_classifier_output",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "category": {
                                    "type": "string",
                                    "enum": ["Produtivo", "Improdutivo"],
                                },
                                "reply": {"type": "string", "minLength": 1},
                            },
                            "required": ["category", "reply"],
                        },
                    }
                },
            )
        except Exception as exc:
            logger.exception("Falha ao chamar a API de IA.")
            raise AIResponseError("Falha ao comunicar com o provedor de IA.") from exc

        payload = self._extract_json_payload(response)
        try:
            return ProcessEmailResponse(**payload)
        except ValidationError as exc:
            raise AIResponseError("A resposta da IA nao respeitou o contrato esperado.") from exc

    def _extract_json_payload(self, response: Any) -> dict[str, Any]:
        raw_text = self._extract_text_response(response)
        if not raw_text:
            raise AIResponseError("A IA retornou uma resposta vazia.")

        try:
            data = json.loads(raw_text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        json_match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError as exc:
                raise AIResponseError("Nao foi possivel interpretar o JSON retornado pela IA.") from exc

        raise AIResponseError("Resposta da IA fora do formato JSON esperado.")

    @staticmethod
    def _extract_text_response(response: Any) -> str:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        output = getattr(response, "output", None)
        if not output:
            return ""

        chunks: list[str] = []
        for item in output:
            content_items = getattr(item, "content", []) or []
            for content in content_items:
                text_value = getattr(content, "text", None)
                if isinstance(text_value, str) and text_value.strip():
                    chunks.append(text_value.strip())
        return "\n".join(chunks).strip()

