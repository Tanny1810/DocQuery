from typing import TypedDict, List, Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.rag.types import RAGDebugMetadata, Source
from app.models import User


class RAGResult(TypedDict):
    answer: str
    sources: List[Source]
    confidence: Optional[float]
    debug: Optional[RAGDebugMetadata]


class RAGStrategy(ABC):
    """
    Base interface for all RAG strategies.
    """

    @abstractmethod
    def run(
        self,
        *,
        db: Session,
        query: str,
        top_k: int,
        user: User,
    ) -> RAGResult:
        """
        Execute the RAG pipeline and return a standardized result.
        """
        pass
