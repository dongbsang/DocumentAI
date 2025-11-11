# Frontend - DocumentAI

React 기반 프론트엔드 웹 애플리케이션

## 📋 디렉토리 구조

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── app/                  # Redux 스토어
│   ├── components/           # 재사용 컴포넌트
│   ├── pages/                # 페이지
│   │   ├── Home.js
│   │   ├── Upload.js
│   │   └── Result.js
│   ├── redux/                # Redux 리듀서 & 사가
│   ├── css/                  # 스타일시트
│   ├── App.jsx
│   └── index.js
├── package.json
└── README.md
```

---

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd frontend
npm install
```

### 2. 개발 서버 실행

```bash
npm start
```

브라우저가 자동으로 `http://localhost:3000`에서 열립니다.

---

## 🔧 주요 기능

### 1. 파일 업로드
- 드래그 앤 드롭 지원
- PDF, 이미지, Word 파일 지원
- 실시간 업로드 진행률 표시

### 2. 문서 카테고리 선택
- 이력서
- 영수증
- 기타

### 3. OCR 옵션
- 손글씨 인식 활성화/비활성화

### 4. 결과 표시
- LLM 분석 결과
- JSON 형식 지원
- 복사/다운로드 기능

---

## 📦 주요 의존성

- **React 19**: UI 라이브러리
- **Redux Toolkit**: 상태 관리
- **React Router**: 라우팅
- **Axios**: HTTP 클라이언트
- **Redux Saga**: 비동기 처리

---

## 🛠️ 스크립트

```bash
# 개발 서버 실행
npm start

# 프로덕션 빌드
npm run build

# 테스트 실행
npm test
```

---

## 🌐 API 통신

### Proxy 설정
`package.json`에서 백엔드 프록시 설정:
```json
{
  "proxy": "http://localhost:5000"
}
```

### API 호출 예시
```javascript
import axios from 'axios';

const uploadFile = async (formData) => {
  const response = await axios.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};
```

---

## 🎨 스타일링

- CSS Modules 사용
- 각 컴포넌트별 독립 스타일시트
- 반응형 디자인 지원

---

## 📱 브라우저 지원

- Chrome (최신)
- Firefox (최신)
- Safari (최신)
- Edge (최신)

---

## ❓ 문제 해결

### 1. 백엔드 연결 실패
```bash
# 백엔드 서버가 실행 중인지 확인
curl http://localhost:5000/api/status
```

### 2. CORS 오류
백엔드의 `flask-cors` 설정을 확인하세요.

### 3. 포트 충돌
```bash
# 다른 포트로 실행
PORT=3001 npm start
```
