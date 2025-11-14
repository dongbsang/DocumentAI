"""
HWP 문서 처리 서비스 (통합 버전)

우선순위:
1. hwp5 라이브러리로 직접 추출 (빠르고 가벼움)
2. olefile로 구버전 HWP 처리 (5.0 이하)
3. LibreOffice로 PDF 변환 후 추출 (최후 수단, 가장 정확)
"""
import tempfile
import shutil
import subprocess
from pathlib import Path
import sys


# ==================== LibreOffice 관련 함수 ====================

def get_libreoffice_path():
    """
    LibreOffice 실행 파일 경로 찾기

    우선순위:
    1. 실행 파일에 포함된 LibreOffice Portable
    2. 시스템에 설치된 LibreOffice

    Returns:
        str: LibreOffice 실행 파일 경로

    Raises:
        RuntimeError: LibreOffice를 찾을 수 없는 경우
    """
    # 1. 실행 파일에 포함된 LibreOffice Portable 확인
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 실행 파일
        base_path = Path(sys._MEIPASS)
    else:
        # 개발 모드
        base_path = Path(__file__).parent.parent.parent.parent

    portable_paths = [
        base_path / "libreoffice" / "program" / "soffice.exe",  # Windows Portable
        base_path / "libreoffice" / "program" / "soffice",      # Linux Portable
    ]

    for path in portable_paths:
        if path.exists():
            print(f"✅ LibreOffice Portable 발견: {path}")
            return str(path)

    # 2. 시스템에 설치된 LibreOffice 확인
    system_paths = [
        # Windows
        "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
        "C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe",
        # Linux
        "/usr/bin/libreoffice",
        "/usr/bin/soffice",
        # macOS
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]

    for path_str in system_paths:
        path = Path(path_str)
        if path.exists():
            print(f"✅ 시스템 LibreOffice 발견: {path}")
            return str(path)

    # 3. PATH 환경 변수에서 찾기
    for cmd in ["libreoffice", "soffice"]:
        cmd_path = shutil.which(cmd)
        if cmd_path:
            print(f"✅ PATH에서 LibreOffice 발견: {cmd_path}")
            return cmd_path

    # 찾지 못함
    raise RuntimeError(
        "LibreOffice를 찾을 수 없습니다.\n"
        "다음 중 하나를 수행하세요:\n"
        "1. https://www.libreoffice.org/download 에서 설치\n"
        "2. LibreOffice Portable을 포함하여 빌드"
    )


def is_libreoffice_available() -> bool:
    """
    LibreOffice 사용 가능 여부 확인

    Returns:
        bool: LibreOffice를 사용할 수 있으면 True
    """
    try:
        get_libreoffice_path()
        return True
    except RuntimeError:
        return False


def convert_hwp_to_pdf(hwp_bytes: bytes, timeout: int = 30) -> bytes:
    """
    LibreOffice를 사용하여 HWP를 PDF로 변환

    Args:
        hwp_bytes: HWP 파일의 바이트 스트림
        timeout: 변환 타임아웃 (초)

    Returns:
        bytes: 변환된 PDF 파일의 바이트 스트림

    Raises:
        RuntimeError: 변환 실패 시
    """
    tmpdir = None
    try:
        print("🔄 HWP → PDF 변환 시작 (LibreOffice 사용)...")

        # LibreOffice 경로 찾기
        try:
            libreoffice_cmd = get_libreoffice_path()
        except RuntimeError as e:
            raise RuntimeError(f"LibreOffice를 찾을 수 없습니다: {str(e)}")

        # 임시 디렉토리 생성
        tmpdir = tempfile.mkdtemp()
        hwp_path = Path(tmpdir) / "input.hwp"

        # HWP 파일 저장
        with open(hwp_path, "wb") as f:
            f.write(hwp_bytes)

        print(f"📝 HWP 파일 저장: {hwp_path} ({len(hwp_bytes):,} bytes)")

        # LibreOffice 변환 실행
        print(f"🔧 LibreOffice 실행: {libreoffice_cmd}")

        result = subprocess.run(
            [
                libreoffice_cmd,
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(tmpdir),
                str(hwp_path)
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # 변환 결과 확인
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "알 수 없는 오류"
            print(f"❌ LibreOffice 변환 실패 (코드: {result.returncode})")
            print(f"   stderr: {result.stderr}")
            print(f"   stdout: {result.stdout}")
            raise RuntimeError(f"LibreOffice 변환 실패: {error_msg}")

        # PDF 파일 확인
        pdf_path = Path(tmpdir) / "input.pdf"

        if not pdf_path.exists():
            # 파일명이 다를 수 있으므로 .pdf 파일 찾기
            pdf_files = list(Path(tmpdir).glob("*.pdf"))
            if pdf_files:
                pdf_path = pdf_files[0]
            else:
                raise RuntimeError("PDF 파일이 생성되지 않았습니다")

        # PDF 파일 읽기
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        print(f"✅ HWP → PDF 변환 완료 ({len(pdf_bytes):,} bytes)")
        return pdf_bytes

    except subprocess.TimeoutExpired:
        print(f"❌ HWP → PDF 변환 시간 초과 ({timeout}초)")
        raise RuntimeError(f"HWP → PDF 변환 시간 초과 ({timeout}초)")

    except Exception as e:
        print(f"❌ HWP → PDF 변환 실패: {str(e)}")
        raise RuntimeError(f"HWP → PDF 변환 실패: {str(e)}")

    finally:
        # 임시 파일 정리
        if tmpdir:
            try:
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception as e:
                print(f"⚠️ 임시 파일 정리 실패: {e}")


# ==================== 메인 HWP 텍스트 추출 함수 ====================

def extract_text_from_hwp(file_bytes: bytes) -> str:
    """
    HWP 파일에서 텍스트 추출
    
    우선순위:
    1. hwp5 직접 추출 (빠름)
    2. olefile 폴백 (구버전 HWP 5.0 이하)
    3. LibreOffice → PDF 변환 (최후 수단, 가장 정확)
    
    Args:
        file_bytes (bytes): HWP 파일의 바이트 스트림
    
    Returns:
        str: 추출된 텍스트
    """
    # 방법 1: hwp5 직접 추출
    try:
        print("📄 방법 1: hwp5로 직접 텍스트 추출 시도...")
        text = extract_text_from_hwp_direct(file_bytes)
        
        if text and text.strip() and len(text.strip()) > 10:
            print(f"✅ hwp5 텍스트 추출 완료 (길이: {len(text)} 자)")
            return text
        else:
            print("⚠️ hwp5 추출 결과가 너무 짧음, olefile로 폴백...")
    
    except Exception as e:
        print(f"⚠️ hwp5 추출 실패: {str(e)}, olefile로 폴백...")
    
    # 방법 2: olefile 폴백 (구버전 HWP)
    try:
        print("📄 방법 2: olefile로 구버전 HWP 처리 시도...")
        text = extract_text_from_hwp_fallback(file_bytes)
        
        if text and text.strip() and len(text.strip()) > 10:
            print(f"✅ olefile 텍스트 추출 완료 (길이: {len(text)} 자)")
            return text
        else:
            print("⚠️ olefile 추출 결과가 너무 짧음, LibreOffice로 폴백...")
    
    except Exception as e:
        print(f"⚠️ olefile 추출 실패: {str(e)}, LibreOffice로 폴백...")
    
    # 방법 3: LibreOffice → PDF 변환 후 추출 (최후 폴백)
    try:
        print("🔄 방법 3: LibreOffice → PDF 변환 후 텍스트 추출 시도...")
        
        if is_libreoffice_available():
            from app.services.pdf_service import extract_text_from_pdf
            
            # HWP → PDF 변환
            pdf_bytes = convert_hwp_to_pdf(file_bytes)
            
            # PDF에서 텍스트 추출
            text = extract_text_from_pdf(pdf_bytes)
            
            if text and text.strip() and len(text.strip()) > 10:
                print(f"✅ LibreOffice → PDF 변환 후 텍스트 추출 완료 (길이: {len(text)} 자)")
                return text
            else:
                print("⚠️ PDF 변환 후 텍스트가 너무 짧음")
        else:
            print("⚠️ LibreOffice를 사용할 수 없습니다")
    
    except Exception as e:
        print(f"⚠️ LibreOffice 변환 실패: {str(e)}")
    
    # 모든 방법 실패
    print("❌ 모든 HWP 텍스트 추출 방법 실패")
    return "[HWP 파일에서 텍스트를 추출할 수 없습니다.]"


# ==================== 보조 추출 함수들 ====================

def extract_text_from_hwp_direct(file_bytes: bytes) -> str:
    """
    hwp5 라이브러리를 사용한 HWP 텍스트 직접 추출
    
    Args:
        file_bytes (bytes): HWP 파일의 바이트 스트림
    
    Returns:
        str: 추출된 텍스트
    """
    tmpdir = None
    try:
        # hwp5는 파일 경로를 요구하므로 임시 파일 생성
        tmpdir = tempfile.mkdtemp()
        hwp_path = Path(tmpdir) / "input.hwp"
        
        # HWP 파일 저장
        with open(hwp_path, "wb") as f:
            f.write(file_bytes)
        
        # hwp5로 텍스트 추출
        try:
            from hwp5.hwp5txt import main as hwp5txt_main
            from io import StringIO
            import sys
            
            # 표준 출력을 캡처
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                # hwp5txt 실행
                hwp5txt_main([str(hwp_path)])
                
                # 결과 가져오기
                result = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            if not result.strip():
                raise ValueError("hwp5 추출 결과가 비어있습니다")
            
            return result.strip()
        
        except ImportError:
            error_msg = "hwp5 라이브러리가 설치되지 않았습니다. pip install hwp5"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
    
    except Exception as e:
        raise ValueError(f"hwp5 추출 실패: {str(e)}")
    
    finally:
        if tmpdir:
            try:
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception:
                pass


def extract_text_from_hwp_fallback(file_bytes: bytes) -> str:
    """
    HWP 파일 텍스트 추출 (fallback 방식 - olefile 사용)
    hwp5 실패 시 구버전 HWP (5.0 이하) 처리
    
    Args:
        file_bytes (bytes): HWP 파일의 바이트 스트림
    
    Returns:
        str: 추출된 텍스트
    """
    try:
        import olefile
        import zlib
        
        print("📄 olefile로 HWP 5.0 이하 형식 처리 중...")
        
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
            print("⚠️ olefile에서도 텍스트를 찾지 못했습니다.")
            return "[HWP 파일에서 텍스트를 추출할 수 없습니다.]"
        
        print(f"✅ olefile 추출 완료 (길이: {len(result)} 자)")
        return result.strip()
    
    except Exception as e:
        error_msg = f"olefile 처리 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return f"[오류] {error_msg}"
