# 🧠 OCR 모델 다운로드 가이드

DocumentAI는 EasyOCR을 사용하여 이미지에서 텍스트를 추출합니다.

## 📦 사전 다운로드 (권장)

첫 실행 전에 OCR 모델을 미리 다운로드하면 나중에 기다릴 필요가 없습니다.

### 방법 1: 자동 다운로드 스크립트 (권장)

```bash
# backend 디렉토리에서
cd backend

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # macOS/Linux

# 모델 다운로드
python download_models.py
```

### 방법 2: Python 직접 실행

```bash
# 가상환경 활성화 후
python
```

```python
>>> import easyocr
>>> reader = easyocr.Reader(['ko', 'en'], gpu=False, verbose=True)
>>> print("✅ 다운로드 완료!")
>>> exit()
```

---

## 📊 다운로드 정보

- **총 용량**: 약 500MB
- **소요 시간**: 5~10분 (인터넷 속도에 따라)
- **저장 위치**: 
  - Windows: `C:\Users\{사용자명}\.EasyOCR\model\`
  - macOS/Linux: `~/.EasyOCR/model/`

---

## 🔍 다운로드 확인

### Windows
```powershell
dir $env:USERPROFILE\.EasyOCR\model\
```

### macOS/Linux
```bash
ls ~/.EasyOCR/model/
```

다음 파일들이 있어야 합니다:
- `craft_mlt_25k.pth` (~90MB)
- `korean_g2.pth` (~50MB)
- `english_g2.pth` (~50MB)
- 기타 파일들

---

## ❓ 문제 해결

### 다운로드가 느린 경우
- 안정적인 인터넷 연결 확인
- VPN 사용 시 비활성화 시도

### 디스크 공간 부족
- 최소 1GB의 여유 공간 필요
- C 드라이브 공간 확인

### 다운로드 중 오류
```bash
pip uninstall easyocr
pip install easyocr
python download_models.py
```

---

## 💡 참고

- 모델은 **첫 실행 시 자동으로 다운로드**됩니다
- 사전 다운로드는 **선택사항**이지만 권장됩니다
- 한 번 다운로드하면 **다시 다운로드할 필요 없습니다**
