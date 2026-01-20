from sqlalchemy.orm import Session

from app.models import User
from app.services.vector_search_service import search_similar_chunks
from app.db.repositories.chunk_repo import get_chunks_for_rag
from app.services.llm_service import call_llm
from shared.rag.prompt_builder import build_prompt

from app.rag.strategies.base import RAGStrategy, RAGResult


class NaiveRAGStrategy(RAGStrategy):
    def run(
        self,
        *,
        db: Session,
        query: str,
        top_k: int,
        user: User,
    ) -> RAGResult:

        # 1️⃣ Vector search
        vector_ids, distances = search_similar_chunks(query, top_k)
        distance_map = dict(zip(vector_ids, distances))

        # 2️⃣ Ownership-safe DB fetch
        rows = get_chunks_for_rag(
            db=db,
            vector_ids=vector_ids,
            current_user=user,
        )

        if not rows:
            return {
                "answer": "I don't know.",
                "sources": [],
                "confidence": 0.0,
            }

        # 3️⃣ Build chunk objects
        chunks = [
            {
                "document_id": row.document_id,
                "chunk_index": row.chunk_index,
                "content": row.content,
                "distance": distance_map.get(row.vector_id, 1.0),
            }
            for row in rows
        ]

        # 4️⃣ Rank by similarity
        chunks.sort(key=lambda x: x["distance"])

        # 5️⃣ Prompt construction
        prompt = build_prompt(query, chunks)

        # 6️⃣ LLM call
        answer = call_llm(prompt)

        return {
            "answer": answer,
            "sources": [
                {
                    "document_id": c["document_id"],
                    "chunk_index": c["chunk_index"],
                }
                for c in chunks
            ],
            "confidence": self._estimate_confidence(chunks),
        }

    def _estimate_confidence(self, chunks: list[dict]) -> float:
        # Simple heuristic for now (V2-safe)
        best_distance = chunks[0]["distance"]
        return max(0.0, min(1.0, 1 - best_distance))
