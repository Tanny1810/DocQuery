from pathlib import Path
from typing import List

from .base import DocumentExtractor
from app.processors.text_extractor import clean_text
from app.processors.types import ExtractedBlock


class TxtExtractor(DocumentExtractor):
    def extract(self, file_path: Path) -> List[ExtractedBlock]:
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

