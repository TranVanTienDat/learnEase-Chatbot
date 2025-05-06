from langchain_core.messages import AIMessage
def extract_content_from_chunk(chunk):
    """
    Lấy content từ 1 chunk
    """
    content = ""
    for message in chunk.get("messages", []):
        if isinstance(message, AIMessage):
            content += message.content or ""
    return content
