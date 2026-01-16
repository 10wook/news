from typing import List, Optional, Callable
from .llm import chat_completion
from .rss import NewsItem
from .crawl import fetch_article_text

SYSTEM_INDIVIDUAL = """너는 뉴스 기사 요약 전문가야.
- 기사 본문을 직접 읽고 정확하게 요약해
- 과장/추측 금지, 기사에 있는 정보만 요약
- 한국어로 간결하게
- 다음 형식으로 요약해:
  제목: [기사 제목]
  핵심 내용: [2-3줄 요약]
  한 줄 요약: [간결한 한 줄 요약]
"""

SYSTEM_SUMMARY = """너는 뉴스 종합 요약 전문가야.
- 여러 기사의 개별 요약을 종합하여 전체 동향을 파악해
- 과장/추측 금지, 기사에 있는 정보만 요약
- 한국어로 간결하게
- 다음 형식으로 작성해:
  1) 전체 동향 요약 (3-5줄)
  2) 주요 기사별 핵심 포인트 (번호 매겨서)
  3) 종합 한 줄 요약
  4) 사용자가 다음에 확인하면 좋을 질문 3개
"""

def summarize_news(items: List[NewsItem], topic: Optional[str], use_crawl: bool = True, progress_callback: Optional[Callable[[str], None]] = None) -> tuple[str, List[str]]:
    # 1단계: 각 기사를 하나하나 읽고 개별 요약
    individual_summaries = []  # 종합 요약용 (간단 버전)
    individual_summaries_display = []  # 화면 표시용 (상세 버전)
    
    for i, it in enumerate(items, start=1):
        if progress_callback:
            progress_callback(f"기사 {i}/{len(items)} 읽는 중: {it.title[:50]}...")
        
        body = ""
        if use_crawl and it.link:
            body = fetch_article_text(it.link)
            if not body:
                # 크롤링 실패 시 RSS 요약 사용
                body = it.summary or ""

        # 본문이 있으면 본문을 우선 사용, 없으면 RSS 요약 사용
        content = body if body else (it.summary or "")
        
        if not content:
            # 내용이 없으면 제목만으로 요약
            individual_summaries.append(f"[{i}] {it.title} - 본문을 가져올 수 없습니다.")
            individual_summaries_display.append(f"**[{i}] {it.title}**\n\n본문을 가져올 수 없습니다.\n\n🔗 [기사 보기]({it.link})")
            continue
        
        # 개별 기사 요약 생성
        try:
            article_prompt = f"""
다음 기사를 읽고 요약해줘:

제목: {it.title}
발행: {it.published or "-"}
본문: {content[:4000] if len(content) > 4000 else content}
""".strip()
            
            individual_summary = chat_completion(
                [
                    {"role": "system", "content": SYSTEM_INDIVIDUAL},
                    {"role": "user", "content": article_prompt},
                ],
                max_completion_tokens=300,
                temperature=None,
            )
            
            # LLM 응답이 None이거나 비어있으면 본문에서 직접 요약 생성
            if not individual_summary or len(individual_summary.strip()) < 10:
                # 본문에서 핵심 문장 추출
                content_clean = content.replace('\n', ' ').strip()
                # 본문의 앞부분과 뒷부분을 조합하여 요약
                if len(content_clean) > 500:
                    preview_start = content_clean[:250]
                    preview_end = content_clean[-150:] if len(content_clean) > 400 else ""
                    content_preview = f"{preview_start}... {preview_end}" if preview_end else preview_start
                else:
                    content_preview = content_clean
                
                individual_summary = f"""제목: {it.title}

핵심 내용: {content_preview}

한 줄 요약: {it.title}에 대한 기사입니다."""
        except Exception as e:
            # 에러 발생 시 기본 요약 사용
            print(f"개별 요약 생성 오류 (기사 {i}): {e}")
            individual_summary = f"핵심 내용: {content[:200] if content else '본문을 가져올 수 없습니다.'}...\n한 줄 요약: {it.title} 관련 기사입니다."
        
        # 종합 요약용 (간단 버전)
        individual_summaries.append(f"[{i}] {it.title}\n{individual_summary}")
        
        # 화면 표시용 (상세 버전)
        individual_summaries_display.append(f"**[{i}] {it.title}**\n\n{individual_summary}\n\n🔗 [기사 보기]({it.link})")
    
    # 2단계: 개별 요약들을 종합하여 종합 요약 생성
    if progress_callback:
        progress_callback("종합 요약 생성 중...")
    
    try:
        combined_prompt = f"""
사용자가 요청한 주제: {topic or "미지정(일반 최신)"}.

아래는 각 기사를 개별적으로 읽고 요약한 결과입니다:

{chr(10).join(individual_summaries)}

위 개별 요약들을 종합하여 전체 동향을 파악하고 종합 요약을 작성해주세요.
""".strip()
        
        final_summary = chat_completion(
            [
                {"role": "system", "content": SYSTEM_SUMMARY},
                {"role": "user", "content": combined_prompt},
            ],
            max_completion_tokens=1200,
            temperature=None,
        )
        
        # LLM 응답이 None이거나 비어있으면 기본 요약 생성
        if not final_summary or len(final_summary.strip()) < 20:
            final_summary = f"""## 전체 동향 요약
{topic or "요청하신 주제"}에 대한 {len(items)}개의 기사를 수집했습니다.

## 주요 기사별 핵심 포인트
{chr(10).join([f"{i+1}. {item.title}" for i, item in enumerate(items)])}

## 종합 한 줄 요약
{topic or "요청하신 주제"} 관련 최신 뉴스를 종합한 결과입니다.

## 추천 질문
1. {topic or "이 주제"}에 대한 더 자세한 정보는 무엇인가요?
2. 최근 {topic or "이 주제"}와 관련된 주요 이슈는 무엇인가요?
3. {topic or "이 주제"}의 향후 전망은 어떤가요?"""
    except Exception as e:
        # 에러 발생 시 기본 요약 사용
        print(f"종합 요약 생성 오류: {e}")
        final_summary = f"""## 전체 동향 요약
{topic or "요청하신 주제"}에 대한 {len(items)}개의 기사를 수집했습니다.

## 주요 기사별 핵심 포인트
{chr(10).join([f"{i+1}. {item.title}" for i, item in enumerate(items)])}

## 종합 한 줄 요약
{topic or "요청하신 주제"} 관련 최신 뉴스를 종합한 결과입니다."""
    
    # 개별 요약과 종합 요약을 함께 반환
    return final_summary, individual_summaries_display