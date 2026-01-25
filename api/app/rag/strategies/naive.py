from sqlalchemy.orm import Session

from app.models import User
from app.services.vector_search_service import search_similar_chunks
from app.db.repositories.chunk_repo import get_chunks_for_rag, search_chunks_bm25
from app.services.llm_service import call_llm
from shared.rag.prompt_builder import build_prompt

from app.rag.strategies.base import RAGStrategy, RAGResult

MAX_PROMPT_CHUNKS = 6


class NaiveRAGStrategy(RAGStrategy):
    def run(
        self,
        *,
        db: Session,
        query: str,
        top_k: int,
        user: User,
    ) -> RAGResult:

        VECTOR_K = top_k
        BM25_K = top_k

        # 1️⃣ Vector retrieval
        vector_ids, distances = search_similar_chunks(query, VECTOR_K)
        vector_distance_map = dict(zip(vector_ids, distances))

        vector_rows = get_chunks_for_rag(
            db=db,
            vector_ids=vector_ids,
            current_user=user,
        )

        # 2️⃣ BM25 retrieval
        bm25_rows = search_chunks_bm25(
            db=db,
            query=query,
            limit=BM25_K,
            current_user=user,
        )

        # 3️⃣ Build chunk objects
        chunks_by_key = {}

        # Vector results
        for row in vector_rows:
            key = (row.document_id, row.chunk_index)
            chunks_by_key[key] = {
                "document_id": row.document_id,
                "chunk_index": row.chunk_index,
                "content": row.content,
                "distance": vector_distance_map.get(row.vector_id, 1.0),
                "bm25_hit": False,
            }

        # BM25 results
        for row in bm25_rows:
            key = (row.document_id, row.chunk_index)
            if key not in chunks_by_key:
                chunks_by_key[key] = {
                    "document_id": row.document_id,
                    "chunk_index": row.chunk_index,
                    "content": row.content,
                    "distance": 1.0,  # no vector distance
                    "bm25_hit": True,
                }
            else:
                chunks_by_key[key]["bm25_hit"] = True

        chunks = list(chunks_by_key.values())

        # 4️⃣ Rank by similarity
        chunks.sort(key=lambda x: x["distance"])

        # 4️⃣.5️⃣ Lightweight reranking (V2-safe)
        chunks = self._rerank_chunks(query=query, chunks=chunks)

        chunks_for_prompt = chunks[:MAX_PROMPT_CHUNKS]

        # 5️⃣ Prompt construction
        prompt = build_prompt(query, chunks_for_prompt)

        # 6️⃣ LLM call
        answer = call_llm(prompt)

        debug_metadata = {
            "retrieved_chunks": [
                {
                    "document_id": str(c["document_id"]),
                    "chunk_index": c["chunk_index"],
                    "distance": c["distance"],
                    "rerank_score": c["rerank_score"],
                }
                for c in chunks
            ],
            "retrieved_count": len(chunks),
            "used_in_prompt": len(chunks_for_prompt),
            "prompt_length": len(prompt),
            "fallback_used": False,
            "bm25_hits": sum(1 for c in chunks if c.get("bm25_hit")),
        }

        return {
            "answer": answer,
            "sources": [
                {
                    "document_id": c["document_id"],
                    "chunk_index": c["chunk_index"],
                }
                for c in chunks_for_prompt
            ],
            "confidence": self._estimate_confidence(chunks_for_prompt),
            "debug": debug_metadata,
        }

    def _estimate_confidence(self, chunks: list[dict]) -> float:
        # Simple heuristic for now (V2-safe)
        best_distance = chunks[0]["distance"]
        return max(0.0, min(1.0, 1 - best_distance))

    def _rerank_chunks(self, *, query: str, chunks: list[dict]) -> list[dict]:
        query_tokens = set(query.lower().split())

        for c in chunks:
            chunk_tokens = set(c["content"].lower().split())

            semantic_score = 1 - c["distance"]
            keyword_overlap = len(query_tokens & chunk_tokens)

            # Penalize very long chunks (simple heuristic)
            length_penalty = min(len(c["content"]) / 1000, 1.0)

            bm25_bonus = 0.1 if c.get("bm25_hit") else 0.0

            c["rerank_score"] = (
                0.7 * semantic_score
                + 0.2 * keyword_overlap
                + bm25_bonus
                - 0.1 * length_penalty
            )

        return sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
