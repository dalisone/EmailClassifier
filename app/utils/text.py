import re

from app.utils.exceptions import EmailValidationError


def preprocess_email_text(raw_text: str, max_chars: int) -> str:
    if not isinstance(raw_text, str):
        raise EmailValidationError("O conteudo do email deve ser texto.")

    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if not text:
        raise EmailValidationError("O conteudo do email esta vazio apos o pre-processamento.")

    if len(text) > max_chars:
        text = text[:max_chars].rstrip()

    return text

