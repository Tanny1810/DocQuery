from app.rag.strategies.naive import NaiveRAGStrategy


class RAGStrategyRegistry:
    _strategies = {
        "naive": NaiveRAGStrategy,
    }

    @classmethod
    def get(cls, mode: str):
        if mode not in cls._strategies:
            raise ValueError(f"Unknown RAG mode: {mode}")
        return cls._strategies[mode]()
