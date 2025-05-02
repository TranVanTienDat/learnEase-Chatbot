import re

def extract_sql_code(text: str) -> str:
    """
    Trích nội dung SQL bên trong block ```sql ... ```
    
    Args:
        text (str): Chuỗi Markdown đầu vào
    
    Returns:
        str: Nội dung SQL (hoặc None nếu không tìm thấy)
    """

    match = re.search(r'```sql\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
