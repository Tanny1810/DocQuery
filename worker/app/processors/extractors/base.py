from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Optional

from app.processors.types import ExtractedBlock


class DocumentExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> List[ExtractedBlock]:
        """
        Must return:
        [
            {
                "text": str,
                "page_number": Optional[int],
                "section_title": Optional[str],
            }
        ]
        """
        raise NotImplementedError
