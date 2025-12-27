from pathlib import Path
from pypdf import PdfReader


def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        return _extract_pdf(file_path)

    elif file_path.suffix.lower() == ".txt":
        return _extract_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


def _extract_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def _extract_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")
