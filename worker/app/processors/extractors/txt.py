from pathlib import Path
from .base import DocumentExtractor
from app.processors.text_extractor import clean_text


class TxtExtractor:
    def extract(self, file_path: Path):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            return []

        return [
            {
                "text": text,
                "page_number": None,
                "section_title": None,
            }
        ]

