import tempfile
from docx2pdf import convert
from pathlib import Path


def convert_docx_to_pdf_bytes(file_bytes: bytes) -> bytes:
    """
    Word(.docx) 파일을 PDF로 변환한 뒤 바이트 형태로 반환
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.docx"
        output_path = Path(tmpdir) / "input.pdf"

        # Save uploaded docx to temp path
        with open(input_path, "wb") as f:
            f.write(file_bytes)

        # Convert using docx2pdf
        convert(str(input_path), str(output_path))

        # Read converted PDF
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()

    return pdf_bytes
