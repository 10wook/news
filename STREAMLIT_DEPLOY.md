# Streamlit Cloud 배포 가이드 (상세)

## 🔍 문제 해결: "Unable to deploy" 오류

오류 메시지: "The app's code is not connected to a remote GitHub repository"

이 오류는 Streamlit Cloud가 GitHub 저장소를 찾지 못할 때 발생합니다.

## ✅ 해결 방법

### 1단계: GitHub 저장소 확인
1. https://github.com/10wook/news 접속
2. 저장소가 Public인지 확인 (Private이면 Streamlit Cloud에서 접근 불가)
3. 저장소에 코드가 있는지 확인 (main 브랜치에 파일들이 있는지)

### 2단계: Streamlit Cloud 권한 확인
1. https://share.streamlit.io 접속
2. GitHub 계정으로 로그인
3. 우측 상단 프로필 아이콘 클릭 → "Settings"
4. "Connected GitHub account" 확인
5. 저장소 권한이 있는지 확인

### 3단계: 저장소 권한 부여 (필요시)
1. Streamlit Cloud Settings → "Repositories"
2. "Add repository" 클릭
3. `10wook/news` 저장소 선택
4. 권한 부여

### 4단계: 앱 배포
1. Streamlit Cloud 메인 페이지에서 "New app" 클릭
2. **Repository**: `10wook/news` 선택
3. **Branch**: `main` 선택
4. **Main file path**: `app.py` 입력
5. **App URL** (선택사항): 원하는 URL 입력 (예: `news-summary-chatbot`)
6. "Deploy!" 클릭

### 5단계: 환경변수 설정 (중요!)
배포가 시작되면:
1. 앱 페이지에서 "⚙️" (Settings) 아이콘 클릭
2. "Secrets" 탭 클릭
3. 다음 내용을 입력:

```
OPENAI_API_KEY=실제_GMS_API_키_여기에_입력
OPENAI_BASE_URL=https://gms.ssafy.io/gmsapi/api.openai.com/v1
OPENAI_MODEL=gpt-5-nano
GOOGLE_NEWS_RSS=https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko
```

4. "Save" 클릭
5. 앱이 자동으로 재배포됩니다

## 🔧 문제 해결 체크리스트

### 저장소가 보이지 않는 경우
- [ ] GitHub 저장소가 Public인지 확인
- [ ] Streamlit Cloud에 GitHub 계정이 연결되어 있는지 확인
- [ ] Streamlit Cloud Settings에서 저장소 권한이 있는지 확인
- [ ] GitHub에서 저장소가 실제로 존재하는지 확인 (https://github.com/10wook/news)

### 배포가 실패하는 경우
- [ ] `app.py` 파일이 저장소 루트에 있는지 확인
- [ ] `requirements.txt` 파일이 있는지 확인
- [ ] 환경변수(Secrets)가 올바르게 설정되었는지 확인
- [ ] 배포 로그 확인 (앱 페이지에서 "Manage app" → "Logs")

### 앱이 실행되지 않는 경우
- [ ] 환경변수(Secrets)가 올바르게 설정되었는지 확인
- [ ] API 키가 유효한지 확인
- [ ] 배포 로그에서 에러 메시지 확인

## 📝 배포 후 확인사항

1. **앱 URL 확인**: Streamlit Cloud에서 제공하는 URL로 접속
2. **기능 테스트**: 
   - 일반 대화 테스트
   - 뉴스 요약 테스트
3. **에러 확인**: 문제가 있으면 로그 확인

## 🆘 추가 도움말

- Streamlit Cloud 문서: https://docs.streamlit.io/streamlit-community-cloud
- GitHub 저장소: https://github.com/10wook/news
