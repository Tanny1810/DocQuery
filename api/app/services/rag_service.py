from app.services.vector_search_service import search_similar_chunks
from app.db.repositories.chunk_repo import get_chunks_for_rag
from app.services.llm_service import call_llm
from shared.rag.prompt_builder import build_prompt


def query_documents(db, query: str, top_k: int):
    # 1️⃣ Vector search
    vector_ids, distances = search_similar_chunks(query, top_k)

    distance_map = dict(zip(vector_ids, distances))

    # 2️⃣ Validate + fetch chunks from DB
    rows = get_chunks_for_rag(db, vector_ids)

    chunks = [
        {
            "document_id": row.document_id,
            "chunk_index": row.chunk_index,
            "content": row.content,
            "score": distance_map.get(row.vector_id, 0.0),
        }
        for row in rows
    ]

    # 3️⃣ Sort by similarity (lower distance = better)
    chunks.sort(key=lambda x: x["score"])

    # 4️⃣ Prompt assembly (token-budget aware)
    prompt = build_prompt(query, chunks)

    # 5️⃣ LLM call
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
    }
