import tiktoken

# Conservative total budget (prompt + context + answer)
TOTAL_TOKEN_BUDGET = 3000
ANSWER_TOKEN_RESERVE = 500  # leave room for generation
CONTEXT_TOKEN_BUDGET = TOTAL_TOKEN_BUDGET - ANSWER_TOKEN_RESERVE

encoder = tiktoken.get_encoding("cl100k_base")


def build_prompt(query: str, chunks: list[dict]) -> str:
    """
    Assemble prompt using highest-similarity chunks first.
    Drops chunks once token budget is exceeded.
    """

    header = (
        "You are an assistant answering questions using ONLY the context below.\n"
        "If the answer is not present, say you don't know.\n\n"
        "Context:\n"
    )

    footer = f"\n\nQuestion:\n{query}\n\nAnswer:\n"

    # Count fixed prompt cost
    fixed_tokens = len(encoder.encode(header + footer))

    context_parts = []
    total_tokens = fixed_tokens

    for chunk in chunks:
        chunk_text = (
            f"[Doc {chunk['document_id']} | Chunk {chunk['chunk_index']}]\n"
            f"{chunk['content']}\n\n"
        )

        chunk_tokens = len(encoder.encode(chunk_text))

        if total_tokens + chunk_tokens > CONTEXT_TOKEN_BUDGET:
            break

        context_parts.append(chunk_text)
        total_tokens += chunk_tokens

    context = "".join(context_parts)

    return (header + context + footer).strip()
