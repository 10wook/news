# 배포 가이드

## GitHub 저장소 생성 및 연결

### 1. GitHub에서 저장소 생성
1. GitHub (https://github.com)에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 이름 입력 (예: `ai-news-summary-chatbot`)
4. Public 또는 Private 선택
5. "Initialize this repository with a README" 체크 해제 (이미 README가 있음)
6. "Create repository" 클릭

### 2. 로컬 저장소와 GitHub 연결
```bash
# GitHub에서 제공하는 저장소 URL 사용 (예: https://github.com/사용자명/저장소명.git)
git remote add origin https://github.com/사용자명/저장소명.git
git branch -M main
git push -u origin main
```

## Streamlit Cloud 배포

### 1. Streamlit Cloud 접속
- https://share.streamlit.io 접속
- GitHub 계정으로 로그인

### 2. 앱 배포
1. "New app" 클릭
2. Repository 선택: 방금 만든 GitHub 저장소 선택
3. Branch: `main` (또는 `master`)
4. Main file path: `app.py`
5. "Deploy!" 클릭

### 3. 환경변수 설정
Streamlit Cloud 대시보드에서:
1. 앱 설정 (Settings) → Secrets
2. 다음 형식으로 입력:
```
OPENAI_API_KEY=실제_GMS_API_키
OPENAI_BASE_URL=https://gms.ssafy.io/gmsapi/api.openai.com/v1
OPENAI_MODEL=gpt-5-nano
GOOGLE_NEWS_RSS=https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko
```

## 로컬에서 GitHub 연결 명령어

```bash
# 저장소 초기화 (이미 완료됨)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: AI 뉴스 요약 챗봇"

# GitHub 저장소 연결 (GitHub에서 저장소 생성 후)
git remote add origin https://github.com/사용자명/저장소명.git
git branch -M main
git push -u origin main
```

## 주의사항
- `.env` 파일은 절대 커밋하지 마세요 (이미 .gitignore에 포함됨)
- API 키는 Streamlit Cloud의 Secrets에만 입력하세요
- 공개 저장소인 경우 API 키가 노출되지 않도록 주의하세요
