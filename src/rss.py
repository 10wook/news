import os
import feedparser
import requests
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NewsItem:
    title: str
    link: str
    published: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None

def fetch_rss(query: Optional[str] = None, limit: int = 8) -> List[NewsItem]:
    base = os.getenv("GOOGLE_NEWS_RSS")
    
    # Google News RSS URL 생성
    if query:
        import urllib.parse
        q = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    elif base:
        url = base
    else:
        url = "https://news.google.com/rss/search?q=AI&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        # User-Agent 헤더 추가하여 요청
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # feedparser로 파싱
        feed = feedparser.parse(response.content)
        
        # 파싱 오류 확인
        if feed.bozo and feed.bozo_exception:
            # 파싱 오류가 있어도 entries가 있으면 사용
            if not feed.entries:
                raise Exception(f"RSS 파싱 오류: {feed.bozo_exception}")
        
        items: List[NewsItem] = []
        for e in feed.entries[:limit]:
            # 제목과 링크가 있는 경우만 추가
            title = getattr(e, "title", "").strip()
            link = getattr(e, "link", "").strip()
            
            # Google News 링크인 경우 실제 URL 추출 시도
            if link and "news.google.com" in link:
                # Google News 링크에서 실제 URL 추출
                # 링크 형식: https://news.google.com/rss/articles/...
                # 실제 URL은 보통 링크 속성에 있음
                if hasattr(e, "links") and e.links:
                    for l in e.links:
                        if l.get("rel") == "alternate" and "news.google.com" not in l.get("href", ""):
                            link = l.get("href", link)
                            break
            
            if title and link:
                items.append(
                    NewsItem(
                        title=title,
                        link=link,
                        published=getattr(e, "published", None),
                        summary=getattr(e, "summary", None),
                        source=getattr(getattr(e, "source", None), "title", None),
                    )
                )
        
        return items
        
    except Exception as e:
        # 에러 발생 시 빈 리스트 반환 (app.py에서 에러 메시지 표시)
        import traceback
        print(f"RSS 가져오기 오류: {e}")
        print(f"URL: {url}")
        traceback.print_exc()
        return []
