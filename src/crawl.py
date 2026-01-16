import requests
from bs4 import BeautifulSoup

def fetch_article_text(url: str, timeout: int = 10) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        # Google News 링크인 경우 리다이렉트를 따라가서 실제 URL 얻기
        if "news.google.com" in url:
            # 세션 사용하여 리다이렉트 추적
            session = requests.Session()
            session.max_redirects = 5
            r = session.get(url, timeout=timeout, headers=headers, allow_redirects=True)
            # 최종 URL 사용
            url = r.url
        else:
            r = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # 인코딩 자동 감지
        soup = BeautifulSoup(r.text, "html.parser")

        # 스크립트와 스타일 태그 제거
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        candidates = []
        # 다양한 셀렉터 시도
        selectors = [
            "article",
            "main article",
            "div.article",
            "div#articleBody",
            "div.article-body",
            "div.article-content",
            "div.content",
            "div#content",
            "div.post-content",
            "div.entry-content",
            "main",
            "div.news_view",
            "div.article_view",
        ]
        
        for sel in selectors:
            nodes = soup.select(sel)
            for node in nodes:
                text = node.get_text(" ", strip=True)
                if len(text) > 200:  # 최소 길이 체크
                    candidates.append(text)

        # 후보가 없으면 body 전체 사용
        if not candidates:
            body = soup.body.get_text(" ", strip=True) if soup.body else ""
            if body:
                candidates.append(body)

        # 가장 긴 텍스트 선택 (일반적으로 본문이 가장 김)
        text = max(candidates, key=len) if candidates else ""
        
        # 불필요한 공백 정리
        text = " ".join(text.split())
        
        return text[:8000]  # 최대 8000자
    except Exception as e:
        # 에러 발생 시 빈 문자열 반환 (RSS 요약으로 폴백)
        return ""
