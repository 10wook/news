# 🗞️ AI 뉴스 요약 챗봇

Streamlit 기반의 AI 뉴스 요약 챗봇 애플리케이션입니다. 일반 대화와 뉴스 요약 기능을 모두 제공합니다.

## ✨ 주요 기능

- **일반 대화**: Friday라는 이름의 긍정적인 AI와 자유롭게 대화할 수 있습니다
- **뉴스 요약**: "AI 뉴스 요약해줘"와 같은 요청으로 최신 뉴스를 수집하고 요약합니다
- **의도 판별**: 규칙 기반 및 LLM 기반 의도 판별 시스템
- **RSS 피드 수집**: Google News RSS를 통해 최신 뉴스 수집
- **기사 본문 크롤링**: 선택적으로 기사 본문을 크롤링하여 더 정확한 요약 제공

## 📋 요구사항

- Python 3.8 이상
- GMS(OpenAI 호환) API 키

## 🚀 설치 및 실행

### 1. 저장소 클론 또는 파일 다운로드

```bash
cd /0116
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 실제 API 키를 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
OPENAI_API_KEY=실제_GMS_API_키
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-5-nano
GOOGLE_NEWS_RSS=https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko
```

**참고**: `.env` 파일이 없어도 실행 시 터미널에서 GMS KEY를 직접 입력할 수 있습니다.

### 4. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며, 열리지 않으면 다음 주소로 접속하세요:
- `http://localhost:8501`
- `http://127.0.0.1:8501`

## 📖 사용 방법

### 일반 대화

채팅 입력창에 일반적인 메시지를 입력하면 Friday AI가 응답합니다.

예시:
- "오늘 기분 어때?"
- "안녕하세요!"
- "파이썬에 대해 알려줘"

### 뉴스 요약

뉴스 관련 키워드가 포함된 메시지를 입력하면 자동으로 뉴스를 수집하고 요약합니다.

예시:
- "AI 뉴스 요약해줘"
- "최신 뉴스 알려줘"
- "기술 뉴스 검색해줘"

### 사이드바 설정

- **의도 판별에 LLM 보조 사용**: LLM을 사용한 의도 판별 활성화/비활성화
- **기사 본문 크롤링 사용**: 기사 본문을 크롤링하여 더 정확한 요약 생성 (선택사항)
- **가져올 기사 수**: RSS에서 가져올 기사 개수 설정 (3~12개)

## 📁 프로젝트 구조

```
.
├── app.py                 # 메인 Streamlit 애플리케이션
├── requirements.txt       # 필요한 패키지 목록
├── .env.example          # 환경변수 예시 파일
├── README.md            # 프로젝트 설명서
└── src/
    ├── __init__.py
    ├── llm.py           # LLM 클라이언트 및 chat_completion
    ├── intent.py        # 의도 판별 로직
    ├── rss.py           # RSS 피드 가져오기
    ├── crawl.py         # 기사 본문 크롤링
    └── summarize.py     # 뉴스 요약 생성
```

## 🔧 환경변수 설명

| 변수명 | 설명 | 필수 | 기본값 |
|--------|------|------|--------|
| `OPENAI_API_KEY` | GMS API 키 | 예 | 없음 (실행 시 입력 가능) |
| `OPENAI_BASE_URL` | GMS base URL | 아니오 | |
| `OPENAI_MODEL` | 사용할 모델명 | 아니오 | `gpt-5-nano` |
| `GOOGLE_NEWS_RSS` | Google News RSS URL | 아니오 | AI 관련 뉴스 RSS |

## 🛠️ 기술 스택

- **Streamlit**: 웹 애플리케이션 프레임워크
- **OpenAI API**: LLM 호출 (GMS 호환)
- **feedparser**: RSS 피드 파싱
- **BeautifulSoup4**: 웹 크롤링
- **python-dotenv**: 환경변수 관리

## 📝 주요 기능 상세

### 의도 판별 (Intent Detection)

1. **규칙 기반**: 키워드 매칭으로 뉴스 검색 의도 판별
   - 키워드: "뉴스", "기사", "헤드라인", "요약", "검색", "최신", "속보", "news"
2. **LLM 기반**: LLM을 사용한 더 정확한 의도 판별 (선택사항)

### 뉴스 수집 및 요약

1. Google News RSS를 통해 최신 뉴스 수집
2. 선택적으로 기사 본문 크롤링
3. LLM을 사용하여 뉴스 요약 생성
4. 전체 동향 요약, 기사별 핵심 포인트, 추천 질문 제공

## ⚠️ 주의사항

- `.env` 파일에는 실제 API 키가 포함되므로 Git에 커밋하지 마세요
- Streamlit 웹 환경에서는 `getpass`가 작동하지 않으므로 `.env` 파일 사용을 권장합니다
- RSS 피드 접근이 차단된 경우 네트워크 설정을 확인하세요

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.
