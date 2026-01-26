from pathlib import Path
from pypdf import PdfReader
from .base import DocumentExtractor
from app.processors.text_extractor import clean_text


class PdfExtractor:
    def extract(self, file_path: Path):
        reader = PdfReader(str(file_path))
        blocks = []

        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                blocks.append(
                    {
                        "text": clean_text(text),
                        "page_number": idx + 1,
                        "section_title": None,
                    }
                )

        return blocks

