from typing import TypedDict, Optional


class ExtractedBlock(TypedDict):
    """
    Canonical output of ALL document extractors.

    One block == one logical text unit
    (page, slide, section, etc.)
    """
    text: str
    page_number: Optional[int]
    section_title: Optional[str]
