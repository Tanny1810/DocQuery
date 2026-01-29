from pathlib import Path
from pypdf import PdfReader
from typing import List

from .base import DocumentExtractor
from app.processors.text_extractor import clean_text
from app.processors.types import ExtractedBlock


class PdfExtractor(DocumentExtractor):
    def extract(self, file_path: Path) -> List[ExtractedBlock]:
        reader = PdfReader(str(file_path))
        blocks: List[ExtractedBlock] = []

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

