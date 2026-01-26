def clean_text(text: str) -> str:
    if not text:
        return text
    return text.replace("\x00", "")
