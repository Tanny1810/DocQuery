import importlib.util
import os
import sys
import types


def _load_builder():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    path = os.path.join(base, "shared", "rag", "prompt_builder.py")
    spec = importlib.util.spec_from_file_location("shared.rag.prompt_builder", path)
    mod = importlib.util.module_from_spec(spec)
    # Inject a lightweight `tiktoken` stub for tests to avoid needing the real package.
    if "tiktoken" not in sys.modules:
        tmod = types.ModuleType("tiktoken")

        def get_encoding(name):
            enc = types.SimpleNamespace()
            enc.encode = lambda s: s.split()
            return enc

        tmod.get_encoding = get_encoding
        sys.modules["tiktoken"] = tmod
    spec.loader.exec_module(mod)
    return mod


def test_prompt_builder_contains_context_and_query():
    mod = _load_builder()
    query = "What happens if energy costs rise?"
    chunks = [
        {
            "document_id": "d1",
            "chunk_index": 0,
            "content": "Energy costs affect production costs",
        },
        {
            "document_id": "d2",
            "chunk_index": 1,
            "content": "Higher energy prices increase inflation",
        },
    ]

    prompt = mod.build_prompt(query=query, chunks=chunks)

    assert query in prompt
    for c in chunks:
        assert c["content"] in prompt
