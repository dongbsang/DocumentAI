"""
HWP 문서 처리 서비스
pyhwp를 사용한 한글 문서 텍스트 추출
"""
import tempfile
import shutil
from pathlib import Path


def extract_text_from_hwp(file_bytes: bytes) -> str:
    """
    HWP 파일에서 텍스트 추출 (pyhwp 사용)

    Args:
        file_bytes (bytes): HWP 파일의 바이트 스트림

    Returns:
        str: 추출된 텍스트
    """
    tmpdir = None
    try:
        print("📄 HWP 파일 → pyhwp로 텍스트 추출 중...")

        # pyhwp는 파일 경로를 요구하므로 임시 파일 생성
        tmpdir = tempfile.mkdtemp()
        hwp_path = Path(tmpdir) / "input.hwp"

        # HWP 파일 저장
        with open(hwp_path, "wb") as f:
            f.write(file_bytes)

        # pyhwp로 텍스트 추출
        try:
            from pyhwp.hwp5 import Hwp5File

            # HWP 파일 열기
            hwp = Hwp5File(str(hwp_path))

            # 텍스트 추출
            text_list = []

            # 모든 섹션 순회
            for section in hwp.bodytext.sections:
                # 각 단락 추출
                for paragraph in section.paragraphs:
                    para_text = paragraph.get_text()
                    if para_text and para_text.strip():
                        text_list.append(para_text.strip())

            hwp.close()

            result = "\n".join(text_list)

            if not result.strip():
                print("⚠️ HWP 파일에서 텍스트를 찾을 수 없습니다.")
                return "[HWP 파일에서 텍스트를 찾을 수 없습니다.]"

            print(f"✅ HWP 텍스트 추출 완료 (길이: {len(result)} 자)")
            return result.strip()

        except ImportError:
            error_msg = "pyhwp 라이브러리가 설치되지 않았습니다. pip install pyhwp 실행"
            print(f"❌ {error_msg}")
            return f"[오류] {error_msg}"

        except Exception as e:
            # pyhwp 실패 시 olefile로 fallback 시도
            print(f"⚠️ pyhwp 추출 실패: {str(e)}, olefile로 재시도...")
            return extract_text_from_hwp_fallback(file_bytes)

    except Exception as e:
        error_msg = f"HWP 파일 읽기 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return f"[오류] {error_msg}"

    finally:
        if tmpdir:
            try:
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception:
                pass


def extract_text_from_hwp_fallback(file_bytes: bytes) -> str:
    """
    HWP 파일 텍스트 추출 (fallback 방식 - olefile 사용)
    pyhwp 실패 시 구버전 HWP (5.0 이하) 처리

    Args:
        file_bytes (bytes): HWP 파일의 바이트 스트림

    Returns:
        str: 추출된 텍스트
    """
    try:
        import olefile
        import zlib

        print("📄 Fallback: olefile로 HWP 5.0 이하 형식 처리 중...")

        # OLE 파일로 열기
        ole = olefile.OleFileIO(file_bytes)

        text_parts = []

        # BodyText 스트림에서 섹션 찾기
        for i in range(100):  # 최대 100개 섹션
            section_name = f'BodyText/Section{i}'

            if not ole.exists(section_name):
                break

            try:
                # 섹션 스트림 읽기
                stream = ole.openstream(section_name)
                data = stream.read()

                # zlib 압축 해제 시도
                try:
                    decompressed = zlib.decompress(data, -15)
                except:
                    decompressed = data

                # UTF-16 LE로 디코딩
                text = decompressed.decode('utf-16-le', errors='ignore')

                # 출력 가능한 문자만 남기기
                clean_text = ''.join(
                    char for char in text
                    if char.isprintable() or char in '\n\r\t '
                )

                if clean_text.strip():
                    text_parts.append(clean_text.strip())

            except Exception as e:
                print(f"⚠️ Section{i} 처리 중 오류: {e}")
                continue

        ole.close()

        result = "\n".join(text_parts)

        if not result.strip():
            print("⚠️ Fallback에서도 텍스트를 찾지 못했습니다.")
            return "[HWP 파일에서 텍스트를 추출할 수 없습니다.]"

        print(f"✅ HWP fallback 추출 완료 (길이: {len(result)} 자)")
        return result.strip()

    except Exception as e:
        error_msg = f"HWP fallback 처리 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return f"[오류] {error_msg}"
