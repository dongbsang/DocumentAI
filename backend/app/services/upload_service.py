from enum import Enum
from pathlib import Path
import mimetypes
import filetype

class FileFormat(str, Enum):
    PDF     = "pdf"
    HWP     = "hwp"
    WORD    = "word"
    IMAGE   = "image"
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
    파일의 포맷을 판별해 FileFormat Enum을 반환합니다.
    - 1차: 확장자 기반
    - 2차: magic bytes (filetype) 기반
    - 3차: mimetypes 모듈 기반
    """
    ext = Path(filename).suffix.lower().lstrip(".")

    # 1) 확장자 기반 우선 판별
    if ext in _EXT_MAP:
        return _EXT_MAP[ext]
    if ext in _IMAGE_EXTS:
        return FileFormat.IMAGE

    # 2) magic bytes 기반 판별
    kind = filetype.guess(file_bytes)
    if kind:
        mime = kind.mime
        if mime == "application/pdf":
            return FileFormat.PDF
        if "wordprocessingml" in mime or "msword" in mime:
            return FileFormat.WORD
        if mime.startswith("image"):
            return FileFormat.IMAGE

    # 3) mimetypes 모듈로 마지막 시도
    mime, _ = mimetypes.guess_type(filename)
    if mime:
        if mime.startswith("image"):
            return FileFormat.IMAGE
        if mime == "application/pdf":
            return FileFormat.PDF
        if mime in ("application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            return FileFormat.WORD

    return FileFormat.UNKNOWN