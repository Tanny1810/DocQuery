from pathlib import Path

from app.processors.extractors.pdf import PdfExtractor
from app.processors.extractors.txt import TxtExtractor


_EXTRACTOR_MAP = {
    ".pdf": PdfExtractor,
    ".txt": TxtExtractor,
}


def get_extractor(file_path: Path):
    suffix = file_path.suffix.lower()

    extractor_cls = _EXTRACTOR_MAP.get(suffix)

    if not extractor_cls:
        raise ValueError(f"Unsupported file type: {suffix}")

    return extractor_cls()
