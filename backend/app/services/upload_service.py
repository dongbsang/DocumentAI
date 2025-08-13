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

_IMAGE_EXTS = {"jpg", "jpeg", "png", "bmp", "tiff", "tif", "gif", "webp"}

def detect_file_format(file_bytes: bytes, filename: str) -> FileFormat:
    mime_type, _ = mimetypes.guess_type(filename)
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    try:
        print(f"파일 확장자: {ext}, MIME 타입: {mime_type}")

        # PDF
        if mime_type == "application/pdf" or ext == "pdf":
            # 안전하게 열기
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                print(f"PDF 페이지 수: {len(doc)}")

                # 암호화된 PDF 처리
                if doc.is_encrypted:
                    try:
                        ok = doc.authenticate("")  # 비밀번호 없는 경우 시도
                    except Exception:
                        ok = False
                    if not ok:
                        # 열리긴 했지만 텍스트 추출 실패 가능성 높음
                        return FileFormat.UNKNOWN_PDF

                # 앞쪽 일부 페이지만 샘플링 (예: 5페이지)
                sample_pages = min(5, len(doc))
                has_text = False
                for i in range(sample_pages):
                    try:
                        text = doc[i].get_text("text")  # ← strip 인자 없음
                        if text and text.strip():
                            has_text = True
                            break
                    except Exception as e:
                        # 개별 페이지 문제는 스킵
                        print(f"페이지 {i} 텍스트 추출 중 오류: {e}")

                print(f"PDF 텍스트 존재 여부: {has_text}")
                return FileFormat.SEARCHABLE_PDF if has_text else FileFormat.SCANNED_PDF

        # 이미지 파일
        if (mime_type and mime_type.startswith("image/")) or ext in _IMAGE_EXTS:
            return FileFormat.IMAGE

        # 한글 문서
        if ext == "hwp":
            return FileFormat.HWP

        # 워드 문서
        if ext in ["doc", "docx"]:
            return FileFormat.WORD

        # 기타
        return FileFormat.UNKNOWN

    except Exception as e:
        print(f"detect_file_format 예외: {e}")
        if ext == "pdf":
            return FileFormat.UNKNOWN_PDF
        return FileFormat.UNKNOWN