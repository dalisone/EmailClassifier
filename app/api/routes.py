import logging
from json import JSONDecodeError
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.api.schemas import ProcessEmailResponse
from app.services.email_processor import EmailProcessorService
from app.utils.config import Settings, get_settings
from app.utils.exceptions import AIResponseError, EmailValidationError, FileProcessingError
from app.utils.file_handlers import extract_text_from_upload
from app.utils.text import preprocess_email_text

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Email Processing"])


@router.post("/process-email", response_model=ProcessEmailResponse)
async def process_email(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> ProcessEmailResponse:
    try:
        email_text = await _extract_email_text_from_request(request)
        normalized_text = preprocess_email_text(email_text, max_chars=settings.max_email_chars)
    except (EmailValidationError, FileProcessingError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payload JSON invalido.",
        ) from exc

    service = EmailProcessorService(settings=settings)
    try:
        result = service.classify_and_reply(normalized_text)
    except AIResponseError as exc:
        logger.exception("Erro no processamento de IA.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Nao foi possivel processar o email com IA no momento.",
        ) from exc

    return result


async def _extract_email_text_from_request(request: Request) -> str:
    content_type = (request.headers.get("content-type") or "").lower()

    if "application/json" in content_type:
        payload = await request.json()
        if not isinstance(payload, dict):
            raise EmailValidationError("Payload JSON deve ser um objeto.")
        email_text = payload.get("email_text")
        if not isinstance(email_text, str) or not email_text.strip():
            raise EmailValidationError("Envie o campo 'email_text' com conteudo valido.")
        return email_text

    form_data = await request.form()
    email_text = form_data.get("email_text")
    uploaded_file = form_data.get("file")

    has_text = isinstance(email_text, str) and bool(email_text.strip())
    has_file = _is_upload_file(uploaded_file)

    if has_text and has_file:
        raise EmailValidationError("Envie somente texto ou arquivo, nao ambos.")

    if not has_text and not has_file:
        raise EmailValidationError("Envie 'email_text' ou um arquivo .txt/.pdf.")

    if has_file:
        return await extract_text_from_upload(uploaded_file)

    return str(email_text)


def _is_upload_file(value: Any) -> bool:
    return isinstance(value, StarletteUploadFile) and bool(value.filename)

