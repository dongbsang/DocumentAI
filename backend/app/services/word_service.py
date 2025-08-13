import os
import time
import shutil
import tempfile, shlex, subprocess
from pathlib import Path
from pathlib import Path
from docx2pdf import convert


def convert_docx_to_pdf_bytes(file_bytes: bytes) -> bytes:
    """
    Word(.docx) -> PDF 바이트
    Windows + MS Word + docx2pdf 기준
    """
    # 임시 디렉터리 수동 관리 (context 종료시 바로 삭제하면 잠금 충돌날 수 있음)
    tmpdir_obj = tempfile.TemporaryDirectory()
    tmpdir = Path(tmpdir_obj.name)
    input_path = tmpdir / "input.docx"
    print(f"[convert] received bytes: {len(file_bytes)} bytes")

    try:
        # 1) DOCX 저장
        with open(input_path, "wb") as f:
            f.write(file_bytes)
        print(f"[convert] saved: {input_path}")

        # 2) 변환 (출력은 디렉터리로 지정)
        print("[convert] launching Word->PDF via docx2pdf ...")
        convert(str(input_path), str(tmpdir))  # <- output을 폴더로
        output_path = tmpdir / f"{input_path.stem}.pdf"

        # Word(COM)가 파일 핸들을 놓는 데 시간이 걸릴 수 있어, 존재/사이즈 확인을 잠깐 재시도
        for i in range(10):
            if output_path.exists() and output_path.stat().st_size > 0:
                break
            time.sleep(0.2)
        else:
            raise RuntimeError("PDF가 생성되지 않았습니다. MS Word 설치/라이선스/권한을 확인하세요.")

        print(f"[convert] PDF ready: {output_path} ({output_path.stat().st_size} bytes)")

        # 3) PDF 바이트 읽기
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()
        if not pdf_bytes:
            raise ValueError("PDF 변환 결과가 비어 있습니다.")

        return pdf_bytes

    finally:
        # 4) 임시폴더 정리 (WinError 32 대비 재시도)
        for i in range(5):
            try:
                tmpdir_obj.cleanup()  # 내부적으로 rmtree 수행
                break
            except PermissionError:
                # 아직 Word가 핸들을 안 놓았을 수 있음
                time.sleep(0.3 * (i + 1))
        else:
            # 그래도 안되면 마지막으로 강제 시도
            try:
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception:
                pass