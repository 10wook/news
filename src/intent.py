from dataclasses import dataclass
from typing import Literal, Optional
from .llm import chat_completion

Intent = Literal["chat", "news_search"]

KEYWORDS = [
    "뉴스", "기사", "헤드라인", "요약", "검색", "최신", "속보", "news"
]

@dataclass
class IntentResult:
    intent: Intent
    topic: Optional[str] = None

def rule_based_intent(user_text: str) -> Optional[IntentResult]:
    t = user_text.strip()
    if any(k.lower() in t.lower() for k in KEYWORDS):
        topic = t
        # 불필요한 단어 제거
        remove_words = KEYWORDS + ["에", "대해서", "찾아보고", "요약해서", "알려줘", "알려", "줘", "해줘", "해주세요", "해서", "하고", "해", "오늘", "내일", "어제", "찾아", "보고"]
        for word in remove_words:
            topic = topic.replace(word, " ")
        topic = " ".join(topic.split()).strip()
        # 너무 짧거나 의미없는 경우 None으로
        if len(topic) < 2:
            topic = None
        return IntentResult(intent="news_search", topic=topic or None)
    return None

def llm_intent(user_text: str) -> IntentResult:
    system = "너는 사용자의 입력이 '일반대화'인지 '뉴스검색요약'인지 분류하는 분류기야. 뉴스검색인 경우 핵심 키워드만 추출해. JSON만 출력해."
    prompt = f"""
사용자 입력: {user_text}

다음 JSON 형식으로만 답해:
{{"intent":"chat"|"news_search","topic":string|null}}

예시:
- "오늘 화재 뉴스에 대해서 찾아보고 요약해서 알려줘" -> {{"intent":"news_search","topic":"화재"}}
- "AI 뉴스 요약해줘" -> {{"intent":"news_search","topic":"AI"}}
- "오늘 기분 어때?" -> {{"intent":"chat","topic":null}}
""".strip()

    out = chat_completion(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=200,
        temperature=None,  # 모델이 temperature를 지원하지 않으므로 None으로 설정
    )

    import json
    try:
        data = json.loads(out)
        intent = data.get("intent", "chat")
        topic = data.get("topic", None)
        if intent not in ("chat", "news_search"):
            intent = "chat"
        return IntentResult(intent=intent, topic=topic)
    except Exception:
        return IntentResult(intent="chat", topic=None)

def detect_intent(user_text: str, use_llm_fallback: bool = True) -> IntentResult:
    r = rule_based_intent(user_text)
    if r:
        return r
    if use_llm_fallback:
        return llm_intent(user_text)
    return IntentResult(intent="chat", topic=None)
