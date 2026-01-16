import os
import getpass
from openai import OpenAI

def get_client() -> OpenAI:
    # GMS Key가 정상적으로 로드되었는지 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = getpass.getpass("GMS KEY를 입력하세요: ")
        os.environ["OPENAI_API_KEY"] = api_key
    
    base_url = os.getenv("OPENAI_BASE_URL", "https://gms.ssafy.io/gmsapi/api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)

def chat_completion(messages, max_completion_tokens=800, temperature=None) -> str:
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    # temperature 파라미터 준비 (None이면 전달하지 않음)
    params = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_completion_tokens,
    }
    
    # temperature가 None이 아니면 추가 (모델이 지원하지 않을 수 있으므로)
    # 일부 모델은 temperature를 지원하지 않으므로 기본값(1)만 사용
    # temperature 파라미터를 제거하여 기본값 사용
    # if temperature is not None:
    #     params["temperature"] = temperature
    
    try:
        res = client.chat.completions.create(**params)
        content = res.choices[0].message.content
        
        # 응답이 비어있거나 None이면 None 반환 (호출자가 처리)
        if not content or len(content.strip()) == 0:
            return None
        
        return content
    except Exception as e:
        print(f"LLM 호출 오류: {e}")
        return None  # None 반환하여 호출자가 처리하도록
