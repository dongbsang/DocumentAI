import pdfplumber
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Args:
        file_bytes (bytes): _description_

    Returns:
        str: _description_
    """
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        print(f"PDF 페이지 수: {len(pdf.pages)}")
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text.strip()
