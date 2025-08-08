import mimetypes
import fitz  # PyMuPDF
from enum import Enum


class FileFormat(str, Enum):
    SEARCHABLE_PDF = "searchable_pdf"
    SCANNED_PDF = "scanned_pdf"
    IMAGE = "image"
    HWP = "hwp"
    WORD = "word"
    UNKNOWN_PDF = "unknown_pdf"
    UNKNOWN = "unknown"


# 확장자 매핑 딕셔너리
_EXT_MAP = {
    "pdf":  FileFormat.PDF,
    "hwp":  FileFormat.HWP,
    "doc":  FileFormat.WORD,
    "docx": FileFormat.WORD,
}
_IMAGE_EXTS = {"jpg", "jpeg", "png", "bmp", "tiff", "tif", "gif", "webp"}


def detect_file_format(file_bytes: bytes, filename: str) -> FileFormat:
    """
    파일 포맷을 자동 판별하여 FileFormat Enum으로 반환합니다.

    - searchable_pdf: 텍스트 기반 PDF
    - scanned_pdf: 이미지 기반 PDF
    - image: PNG, JPG 등 이미지 파일
    - word: .doc, .docx
    - hwp: .hwp
    - unknown_pdf: PDF 열기 실패
    - unknown: 미지원 포맷
    """
    mime_type, _ = mimetypes.guess_type(filename)
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    try:
        # PDF
        if mime_type == "application/pdf" or ext == "pdf":
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            has_text = any(page.get_text(strip=True) for page in doc)
            return FileFormat.SEARCHABLE_PDF if has_text else FileFormat.SCANNED_PDF
        # 이미지 파일
        elif (mime_type and mime_type.startswith("image/")) or ext in ["jpg", "jpeg", "png", "bmp", "tiff", "gif"]:
            return FileFormat.IMAGE
        # 한글 문서
        elif ext == "hwp":
            return FileFormat.HWP
        # 워드 문서
        elif ext in ["doc", "docx"]:
            return FileFormat.WORD
        # 그 외
        else:
            return FileFormat.UNKNOWN

    except Exception:
        if ext == "pdf":
            return FileFormat.UNKNOWN_PDF
        return FileFormat.UNKNOWN
