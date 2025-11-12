import pdfplumber
import fitz
from io import BytesIO
import logging
from app.utils.exceptions import FileProcessingError

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    PDF 파일에서 텍스트를 추출합니다.

    Args:
        file_bytes: PDF 파일의 바이트 스트림

    Returns:
        str: 추출된 전체 텍스트

    Raises:
        FileProcessingError: PDF 처리 중 오류 발생 시
    """
    if not file_bytes:
        raise FileProcessingError(
            message="PDF 파일 데이터가 비어있습니다",
            details="파일 크기가 0바이트입니다"
        )

    text = ""

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"📄 PDF 페이지 수: {total_pages}")

            if total_pages == 0:
                raise FileProcessingError(
                    message="PDF 파일에 페이지가 없습니다",
                    details="파일이 손상되었을 수 있습니다"
                )

            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text() or ""
                    logger.debug(f"  └ [Page {i+1}] 글자 수: {len(page_text)}")
                    text += page_text + "\n"
                except Exception as page_error:
                    logger.warning(f"⚠️ 페이지 {i+1} 추출 실패: {page_error}")
                    # 개별 페이지 실패는 계속 진행
                    continue

        if not text.strip():
            logger.warning("⚠️ 텍스트가 없는 PDF입니다")
            raise FileProcessingError(
                message="PDF에서 텍스트를 추출하지 못했습니다",
                details="이미지 기반 PDF일 가능성이 높습니다. OCR 처리를 시도하세요."
            )

        logger.info(f"✅ PDF 텍스트 추출 완료: {len(text)} 자")
        return text.strip()

    except FileProcessingError:
        # 이미 처리된 에러는 그대로 전파
        raise

    except Exception as e:
        logger.error(f"❌ PDF 텍스트 추출 중 예상치 못한 오류: {str(e)}")
        raise FileProcessingError(
            message="PDF 처리 중 오류가 발생했습니다",
            details=f"오류 내용: {str(e)}"
        )


def extract_images_from_pdf(file_bytes: bytes, dpi: int = 300) -> list[bytes]:
    """
    스캔 PDF에서 각 페이지를 이미지로 추출합니다.

    Args:
        file_bytes: PDF 파일의 바이트 스트림
        dpi: 렌더링 해상도 (기본 300)

    Returns:
        list[bytes]: 각 페이지의 이미지 리스트

    Raises:
        FileProcessingError: PDF 이미지 추출 중 오류 발생 시
    """
    if not file_bytes:
        raise FileProcessingError(
            message="PDF 파일 데이터가 비어있습니다",
            details="파일 크기가 0바이트입니다"
        )

    images = []

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        total_pages = len(doc)
        logger.info(f"📄 스캔 PDF 이미지 추출 - 총 {total_pages}페이지")

        if total_pages == 0:
            raise FileProcessingError(
                message="PDF 파일에 페이지가 없습니다",
                details="파일이 손상되었을 수 있습니다"
            )

        for i, page in enumerate(doc):
            try:
                pix = page.get_pixmap(dpi=dpi)
                img_bytes = pix.tobytes("png")
                logger.debug(f"  └ [Page {i+1}] 이미지 크기: {len(img_bytes):,} bytes")
                images.append(img_bytes)
            except Exception as page_error:
                logger.error(f"❌ 페이지 {i+1} 이미지 추출 실패: {page_error}")
                raise FileProcessingError(
                    message=f"PDF 페이지 {i+1} 이미지 추출 실패",
                    details=str(page_error)
                )

        if not images:
            raise FileProcessingError(
                message="PDF에서 이미지를 추출하지 못했습니다",
                details="모든 페이지 추출에 실패했습니다"
            )

        logger.info(f"✅ PDF 이미지 추출 완료: {len(images)}개 페이지")
        return images

    except FileProcessingError:
        raise

    except Exception as e:
        logger.error(f"❌ PDF 이미지 추출 중 예상치 못한 오류: {str(e)}")
        raise FileProcessingError(
            message="PDF 이미지 추출 중 오류가 발생했습니다",
            details=f"오류 내용: {str(e)}"
        )
