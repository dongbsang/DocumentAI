"""
Word 문서 처리 서비스
"""
import struct
from io import BytesIO
from docx import Document
import olefile


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    .docx 파일에서 직접 텍스트 추출 (MS Word 불필요!)
    python-docx 라이브러리 사용

    Args:
        file_bytes (bytes): .docx 파일의 바이트 스트림

    Returns:
        str: 추출된 텍스트
    """
    try:
        print("📄 .docx 파일 → python-docx로 직접 텍스트 추출 중...")

        # BytesIO로 메모리에서 직접 처리
        doc = Document(BytesIO(file_bytes))

        # 모든 단락의 텍스트 추출
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:  # 빈 줄 제외
                paragraphs.append(text)

        # 표(table) 내용도 추출
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text:
                        paragraphs.append(text)

        result = "\n".join(paragraphs)
        print(f"✅ .docx 텍스트 추출 완료 (길이: {len(result)} 자)")

        if not result.strip():
            return "[.docx 파일에서 텍스트를 찾을 수 없습니다.]"

        return result.strip()

    except Exception as e:
        print(f"❌ .docx 텍스트 추출 오류: {str(e)}")
        return f"[.docx 파일 읽기 실패: {str(e)}]"


def extract_text_from_doc(file_bytes: bytes) -> str:
    """
    .doc 파일에서 텍스트 추출 (olefile 사용)
    MS Word 97-2003 형식 (.doc)은 OLE (Object Linking and Embedding) 구조
    olefile 라이브러리로 WordDocument 스트림에서 텍스트 추출
    Args:
        file_bytes (bytes): .doc 파일의 바이트 스트림
    Returns:
        str: 추출된 텍스트
    """
    try:
        print("📄 .doc 파일 → olefile로 텍스트 추출 중...")

        # OLE 파일 열기
        ole = olefile.OleFileIO(file_bytes)

        # WordDocument 스트림 읽기
        if not ole.exists('WordDocument'):
            print("⚠️ WordDocument 스트림을 찾을 수 없습니다.")
            return "[.doc 파일 형식이 올바르지 않습니다.]"

        # WordDocument 스트림에서 텍스트 추출
        word_stream = ole.openstream('WordDocument')
        data = word_stream.read()

        # 텍스트 시작 위치와 길이 추출
        try:
            # FIB 구조에서 텍스트 정보 읽기
            # 0x18 오프셋: fcMin (텍스트 시작 위치)
            # 0x1C 오프셋: ccpText (문자 개수)
            fc_min = struct.unpack('<I', data[0x18:0x1C])[0]
            ccp_text = struct.unpack('<I', data[0x4C:0x50])[0]

            # 텍스트 추출
            text_start = fc_min
            text_end = text_start + (ccp_text * 2)

            if text_end > len(data):
                text_end = len(data)

            # 텍스트 디코딩 (Unicode)
            raw_text = data[text_start:text_end]
            text = raw_text.decode('utf-16-le', errors='ignore')

            # 제어 문자 제거
            text = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
            text = text.strip()

            ole.close()

            if not text:
                print("⚠️ .doc 파일에서 텍스트를 추출하지 못했습니다.")
                return "[.doc 파일에서 텍스트를 찾을 수 없습니다.]"

            print(f"✅ .doc 텍스트 추출 완료 (길이: {len(text)} 자)")
            return text

        except Exception as parse_error:
            print(f"⚠️ .doc 파싱 중 오류: {str(parse_error)}")
            ole.close()

            # fallback: 바이너리에서 직접 텍스트 추출 시도
            print("📄 fallback: 바이너리에서 직접 텍스트 추출 시도...")
            return extract_text_from_doc_fallback(file_bytes)

    except Exception as e:
        print(f"❌ .doc 파일 읽기 오류: {str(e)}")
        return f"[.doc 파일 읽기 실패: {str(e)}]"


def extract_text_from_doc_fallback(file_bytes: bytes) -> str:
    """
    .doc 파일에서 텍스트 추출 (fallback 방식)
    바이너리 데이터에서 출력 가능한 문자열 추출
    Args:
        file_bytes (bytes): .doc 파일의 바이트 스트림
    Returns:
        str: 추출된 텍스트
    """
    try:
        # UTF-16 LE로 디코딩 시도
        text = file_bytes.decode('utf-16-le', errors='ignore')

        # 출력 가능한 문자만 남기기
        printable_text = ''.join(
            char for char in text
            if char.isprintable() or char in '\n\r\t '
        )

        # 연속된 공백/줄바꿈 정리
        lines = []
        for line in printable_text.split('\n'):
            line = ' '.join(line.split())  # 연속 공백 제거
            if len(line) > 3:  # 의미 있는 텍스트만 (3자 이상)
                lines.append(line)

        result = '\n'.join(lines)

        if result.strip():
            print(f"✅ .doc fallback 추출 완료 (길이: {len(result)} 자)")
            return result.strip()
        else:
            print("⚠️ .doc fallback에서도 텍스트를 찾지 못했습니다.")
            return "[.doc 파일에서 텍스트를 추출할 수 없습니다.]"

    except Exception as e:
        print(f"❌ .doc fallback 오류: {str(e)}")
        return f"[.doc 파일 읽기 실패: {str(e)}]"
