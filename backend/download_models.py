"""
EasyOCR 모델 사전 다운로드 스크립트

이 스크립트는 EasyOCR에서 사용하는 한글과 영어 인식 모델을 미리 다운로드합니다.
첫 실행 시 약 500MB 정도의 모델을 다운로드하므로 시간이 걸릴 수 있습니다.
"""

import easyocr
import os


def download_easyocr_models():
    """
    EasyOCR 한글 + 영어 모델 다운로드
    """
    print("=" * 60)
    print("EasyOCR 모델 다운로드 시작")
    print("=" * 60)
    print()

    # 다운로드될 경로 출력
    model_storage_directory = os.path.expanduser('~/.EasyOCR/model')
    print(f"📂 모델 저장 경로: {model_storage_directory}")
    print()

    try:
        print("🔽 한글 + 영어 모델 다운로드 중...")
        print("   (첫 실행 시 약 500MB 다운로드, 시간이 걸릴 수 있습니다)")
        print()

        # GPU 사용 안 함 (CPU 모드)
        reader = easyocr.Reader(['ko', 'en'], gpu=False, verbose=True)

        print()
        print("=" * 60)
        print("✅ EasyOCR 모델 다운로드 완료!")
        print("=" * 60)
        print()

        # 테스트
        print("🧪 간단한 테스트 실행 중...")
        test_result = reader.readtext('test', detail=0)
        print("✅ 모델 로드 테스트 성공!")
        print(test_result)

        # 다운로드된 파일 확인
        if os.path.exists(model_storage_directory):
            print(f"📦 다운로드된 파일:")
            for file in os.listdir(model_storage_directory):
                file_path = os.path.join(model_storage_directory, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"   - {file} ({size_mb:.2f} MB)")

        print()
        print("🎉 이제 OCR을 사용할 준비가 완료되었습니다!")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print()
        print("💡 문제 해결 방법:")
        print("   1. 인터넷 연결을 확인하세요")
        print("   2. 가상환경이 활성화되어 있는지 확인하세요")
        print("   3. pip install easyocr 로 재설치를 시도하세요")
        return False

    return True


if __name__ == "__main__":
    success = download_easyocr_models()

    if success:
        print()
        print("=" * 60)
        print("다음 단계:")
        print("=" * 60)
        print("1. flask run 으로 서버를 실행하세요")
        print("2. 프론트엔드에서 이미지를 업로드하여 OCR을 테스트하세요")
        print("=" * 60)

    input("\n아무 키나 눌러 종료하세요...")
