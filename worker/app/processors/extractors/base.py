from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict


class DocumentExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> List[Dict]:
        """
        Must return:
        [
            {
                "content": str,
                "page_number": Optional[int],
                "section_title": Optional[str],
            }
        ]
        """
        pass
