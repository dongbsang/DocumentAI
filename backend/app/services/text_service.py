"""
텍스트 파일 처리 서비스
TXT 파일에서 텍스트를 추출하고 인코딩을 자동으로 감지합니다.
"""
import chardet


def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    TXT 파일에서 텍스트를 추출합니다.
    UTF-8, EUC-KR, CP949 등 자동 인코딩 감지
    Args:
        file_bytes (bytes): TXT 파일의 바이트 스트림

    Returns:
        str: 추출된 텍스트
    """
    try:
        # 1단계: chardet으로 인코딩 자동 감지
        detected = chardet.detect(file_bytes)
        encoding = detected.get('encoding', 'utf-8')
        confidence = detected.get('confidence', 0)

        print(f"📝 감지된 인코딩: {encoding} (신뢰도: {confidence:.2f})")

        # 2단계: 감지된 인코딩으로 디코딩 시도
        if encoding and confidence > 0.7:
            try:
                text = file_bytes.decode(encoding)
                print(f"✅ {encoding} 인코딩으로 디코딩 성공")
                return text.strip()
            except (UnicodeDecodeError, LookupError):
                print(f"⚠️ {encoding} 디코딩 실패, UTF-8로 재시도...")

        # 3단계: UTF-8 fallback
        try:
            text = file_bytes.decode('utf-8')
            print("✅ UTF-8 디코딩 성공")
            return text.strip()
        except UnicodeDecodeError:
            print("⚠️ UTF-8 실패, EUC-KR 시도...")

        # 4단계: EUC-KR/CP949 fallback (한국어)
        try:
            text = file_bytes.decode('euc-kr')
            print("✅ EUC-KR 디코딩 성공")
            return text.strip()
        except UnicodeDecodeError:
            try:
                text = file_bytes.decode('cp949')
                print("✅ CP949 디코딩 성공")
                return text.strip()
            except UnicodeDecodeError:
                pass

        # 5단계: 최종 fallback (에러 무시)
        text = file_bytes.decode('utf-8', errors='ignore')
        print("⚠️ 일부 문자가 손실될 수 있습니다 (errors='ignore' 적용)")
        return text.strip()

    except Exception as e:
        print(f"❌ 텍스트 파일 읽기 오류: {str(e)}")
        return "[텍스트 파일을 읽을 수 없습니다.]"
