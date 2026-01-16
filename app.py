import streamlit as st
from dotenv import load_dotenv

from src.intent import detect_intent
from src.rss import fetch_rss
from src.summarize import summarize_news
from src.llm import chat_completion

load_dotenv()

st.set_page_config(page_title="AI 뉴스 요약 챗봇", page_icon="🗞️")

with st.sidebar:
    st.header("설정")
    use_llm_intent = st.checkbox("의도 판별에 LLM 보조 사용", value=True)
    use_crawl = st.checkbox("기사 본문 크롤링 사용", value=True)
    rss_limit = st.slider("가져올 기사 수", 3, 12, 8)
    st.divider()
    st.caption("환경변수(.env): OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL / GOOGLE_NEWS_RSS")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "당신은 Friday라는 이름의 긍정 에너지 가득한 AI입니다. 사용자를 친절하게 돕되, 뉴스 요약 요청이 오면 정확하고 간결하게 요약합니다.",
        }
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🗞️ Streamlit 기반 AI 뉴스 요약 챗봇")
st.caption("일반 대화도 가능하고, 'AI 뉴스 요약해줘'처럼 말하면 최신 기사 요약을 해줘요.")

for m in st.session_state.chat_history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_text = st.chat_input("메시지를 입력하세요 (예: 'AI 뉴스 요약해줘' / '오늘 기분 어때?')")

if user_text:
    st.session_state.chat_history.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    intent_res = detect_intent(user_text, use_llm_fallback=use_llm_intent)

    if intent_res.intent == "news_search":
        topic = intent_res.topic or "최신 뉴스"

        with st.chat_message("assistant"):
            with st.spinner("뉴스 수집 중..."):
                items = fetch_rss(query=topic, limit=rss_limit)

            if not items:
                st.error(f"뉴스를 가져오지 못했어요. 검색어: '{topic}'\nRSS 주소나 네트워크 상태를 확인해 주세요.")
                st.info("💡 팁: 검색어를 간단하게 입력해보세요 (예: '화재', 'AI', '경제')")
            else:
                # 진행 상황 표시를 위한 상태 변수
                status_text = st.empty()
                progress_bar = st.progress(0)
                
                def update_progress(message: str):
                    status_text.text(message)
                
                # 각 기사를 하나하나 읽고 요약한 후 종합 요약 생성
                final_summary, individual_summaries = summarize_news(
                    items, 
                    topic=topic, 
                    use_crawl=use_crawl,
                    progress_callback=update_progress
                )
                
                progress_bar.progress(1.0)
                status_text.empty()
                progress_bar.empty()

                # 개별 기사 요약 표시
                st.markdown("### 📰 개별 기사 요약")
                for individual_summary in individual_summaries:
                    st.markdown(individual_summary)
                    st.markdown("---")
                
                # 종합 요약 표시
                st.markdown("### 📊 종합 요약")
                st.markdown(final_summary)

                # 채팅 히스토리에 저장 (개별 요약 + 종합 요약)
                full_content = "### 📰 개별 기사 요약\n\n"
                for individual_summary in individual_summaries:
                    full_content += individual_summary + "\n\n---\n\n"
                full_content += "### 📊 종합 요약\n\n" + final_summary
                
                st.session_state.chat_history.append({"role": "assistant", "content": full_content})

    else:
        st.session_state.messages.append({"role": "user", "content": user_text})

        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                assistant_text = chat_completion(
                    st.session_state.messages,
                    max_completion_tokens=700,
                    temperature=None,  # 모델이 temperature를 지원하지 않으므로 None으로 설정
                )
            st.markdown(assistant_text)

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
