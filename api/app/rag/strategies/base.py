from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models import User


class RAGResult(dict):
    """
    Standardized RAG response contract.
    """
    # {
    #   "answer": str,
    #   "sources": list[dict],
    #   "confidence": float | None,
    #   "debug": dict | None
    # }


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
