import pdfplumber
import fitz
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    PDF 파일에서 텍스트를 추출합니다. 텍스트 기반 PDF에서만 작동합니다.

    Args:
        file_bytes (bytes): PDF 파일의 바이트 스트림

    Returns:
        str: 추출된 전체 텍스트. 텍스트가 없을 경우 안내 메시지를 반환합니다.
    """
    text = ""

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            total_pages = len(pdf.pages)
            print(f"📄 PDF 페이지 수: {total_pages}")

            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                print(f"  └ [Page {i+1}] 글자 수: {len(page_text)}")
                text += page_text + "\n"

        if not text.strip():
            print("⚠️ 텍스트가 없는 PDF입니다. (이미지 기반일 수 있음)")
            return "[텍스트를 추출하지 못했습니다.]"

        return text.strip()

    except Exception as e:
        print(f"❌ PDF 텍스트 추출 중 오류 발생: {str(e)}")
        return "[PDF 텍스트 추출 중 오류가 발생했습니다.]"


def extract_images_from_pdf(file_bytes: bytes, dpi: int = 300) -> list[bytes]:
    """
    스캔 PDF에서 각 페이지를 이미지(PNG)로 추출하여 bytes 형태로 반환합니다.

    Args:
        file_bytes (bytes): PDF 파일의 바이트 스트림
        dpi (int): 렌더링 해상도 (기본 300)

    Returns:
        list[bytes]: 각 페이지의 이미지 (PNG format) 리스트
    """
    images = []

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        print(f"📄 스캔 PDF 이미지 추출 - 총 {len(doc)}페이지")

        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)  # 고해상도 렌더링
            img_bytes = pix.tobytes("png")
            print(f"  └ [Page {i+1}] 이미지 크기: {len(img_bytes):,} bytes")
            images.append(img_bytes)

        if not images:
            print("⚠️ 추출된 이미지가 없습니다.")
        return images

    except Exception as e:
        print(f"❌ PDF 이미지 추출 중 오류 발생: {str(e)}")
        return []
