import io
from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader

from app.utils.exceptions import FileProcessingError


ALLOWED_EXTENSIONS = {".txt", ".pdf"}


async def extract_text_from_upload(upload_file: UploadFile) -> str:
    if not upload_file or not upload_file.filename:
        raise FileProcessingError("Arquivo nao enviado ou nome de arquivo invalido.")

    extension = Path(upload_file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise FileProcessingError("Formato nao suportado. Envie apenas arquivos .txt ou .pdf.")

    raw_bytes = await upload_file.read()
    if not raw_bytes:
        raise FileProcessingError("Arquivo enviado esta vazio.")

    if extension == ".txt":
        return _extract_text_from_txt(raw_bytes)

    if extension == ".pdf":
        return _extract_text_from_pdf(raw_bytes)

    raise FileProcessingError("Nao foi possivel processar o arquivo enviado.")


def _extract_text_from_txt(raw_bytes: bytes) -> str:
    for encoding in ("utf-8", "latin-1"):
        try:
            text = raw_bytes.decode(encoding)
            if text.strip():
                return text
        except UnicodeDecodeError:
            continue
    raise FileProcessingError("Nao foi possivel decodificar o arquivo .txt enviado.")


def _extract_text_from_pdf(raw_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(raw_bytes))
        pages_text = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:
        raise FileProcessingError("Falha ao ler o arquivo PDF.") from exc

    text = "\n".join(pages_text).strip()
    if not text:
        raise FileProcessingError("Nao foi encontrado texto legivel no arquivo PDF.")
    return text

