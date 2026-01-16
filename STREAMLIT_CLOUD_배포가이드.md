# 🚀 Streamlit Cloud 배포 완벽 가이드

## 📋 사전 준비사항

✅ **완료된 항목:**
- GitHub 저장소 생성: https://github.com/10wook/news
- 코드 푸시 완료
- `app.py` 파일 존재
- `requirements.txt` 파일 존재

## 🎯 배포 단계별 가이드

### 1단계: Streamlit Cloud 접속 및 로그인

1. **웹 브라우저에서 접속**
   - https://share.streamlit.io 접속
   - 또는 https://streamlit.io/cloud 접속

2. **GitHub 계정으로 로그인**
   - "Sign in" 또는 "Get started" 버튼 클릭
   - GitHub 계정 선택
   - GitHub 로그인 화면에서 인증
   - Streamlit Cloud 권한 부여 승인

### 2단계: 저장소 권한 확인 및 부여

1. **Settings 확인**
   - Streamlit Cloud 대시보드 우측 상단 프로필 아이콘 클릭
   - "Settings" 선택

2. **저장소 권한 확인**
   - "Repositories" 탭 클릭
   - `10wook/news` 저장소가 목록에 있는지 확인

3. **저장소가 보이지 않는 경우**
   - "Add repository" 버튼 클릭
   - `10wook/news` 저장소 선택
   - "Install" 또는 "Authorize" 클릭
   - GitHub에서 권한 승인

### 3단계: 새 앱 배포

1. **앱 생성**
   - Streamlit Cloud 메인 페이지에서
   - "New app" 버튼 클릭 (우측 상단 또는 중앙)

2. **앱 설정 입력**
   ```
   Repository: 10wook/news
   Branch: main
   Main file path: app.py
   App URL: (선택사항) 원하는 URL 입력 (예: news-summary-chatbot)
   ```

3. **배포 시작**
   - "Deploy!" 버튼 클릭
   - 배포가 시작됩니다 (1-2분 소요)

### 4단계: 환경변수 설정 (중요!)

배포가 시작되면 즉시 환경변수를 설정해야 합니다:

1. **Settings 열기**
   - 앱 페이지에서 "⚙️" (Settings) 아이콘 클릭
   - 또는 "Manage app" → "Settings"

2. **Secrets 탭 선택**
   - "Secrets" 탭 클릭

3. **환경변수 입력**
   - 다음 형식으로 입력:
   ```
   OPENAI_API_KEY=실제_GMS_API_키_여기에_입력
   OPENAI_BASE_URL=https://gms.ssafy.io/gmsapi/api.openai.com/v1
   OPENAI_MODEL=gpt-5-nano
   GOOGLE_NEWS_RSS=https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko
   ```

4. **저장**
   - "Save" 버튼 클릭
   - 앱이 자동으로 재배포됩니다

### 5단계: 배포 확인

1. **배포 상태 확인**
   - 앱 페이지에서 배포 상태 확인
   - "Running" 상태가 되면 완료

2. **앱 접속**
   - 제공된 URL로 접속 (예: `https://news-summary-chatbot.streamlit.app`)
   - 또는 앱 페이지에서 "Open app" 클릭

3. **기능 테스트**
   - 일반 대화 테스트
   - 뉴스 요약 테스트

## 🔧 문제 해결

### 문제 1: "Unable to deploy" 오류

**원인:**
- 저장소 권한이 없음
- 저장소가 Private임
- 저장소를 찾을 수 없음

**해결:**
1. Settings → Repositories에서 저장소 권한 확인
2. GitHub에서 저장소가 Public인지 확인
3. 저장소 이름이 정확한지 확인 (`10wook/news`)

### 문제 2: 저장소가 목록에 없음

**해결:**
1. Settings → Repositories → "Add repository"
2. `10wook/news` 검색
3. "Install" 클릭
4. GitHub에서 권한 승인

### 문제 3: 배포 실패

**확인사항:**
1. `app.py` 파일이 루트에 있는지 확인
2. `requirements.txt` 파일이 있는지 확인
3. "Manage app" → "Logs"에서 에러 메시지 확인

### 문제 4: 앱이 실행되지 않음

**확인사항:**
1. Secrets에 환경변수가 올바르게 설정되었는지 확인
2. API 키가 유효한지 확인
3. 로그에서 에러 메시지 확인

## 📝 배포 후 관리

### 코드 업데이트
1. 로컬에서 코드 수정
2. Git 커밋 및 푸시
3. Streamlit Cloud가 자동으로 재배포

### 환경변수 수정
1. Settings → Secrets
2. 값 수정 후 "Save"
3. 자동 재배포

### 앱 삭제
1. "Manage app" → "Settings"
2. 맨 아래 "Delete app" 클릭
3. 확인

## 🎉 완료!

배포가 완료되면:
- ✅ 공개 URL로 앱 접속 가능
- ✅ 자동 재배포 (코드 푸시 시)
- ✅ 무료 호스팅
- ✅ HTTPS 지원

## 📞 추가 도움말

- Streamlit Cloud 문서: https://docs.streamlit.io/streamlit-community-cloud
- GitHub 저장소: https://github.com/10wook/news
- Streamlit 공식 사이트: https://streamlit.io
