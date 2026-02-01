import autogen
import os

# 1. LLM 설정 (OAI_CONFIG_LIST 파일에서 설정을 가져옵니다)
# OAI_CONFIG_LIST.json.template 파일을 복사하여 OAI_CONFIG_LIST 파일을 만드세요.
config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4o", "gpt-4-turbo-preview"],
    },
)

# 2. Assistant 에이전트 생성 (문제 해결사)
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 42,  # 결과 재현성을 위해 캐시 사용
        "config_list": config_list,
        "temperature": 0,
    },
)

# 3. UserProxy 에이전트 생성 (코드 실행기)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # 로컬 환경에서 실행 (주의!)
    },
)

# 4. 작업 시작
user_proxy.initiate_chat(
    assistant,
    message="""
    1. yfinance 라이브러리를 사용하여 NVIDIA(NVDA)와 Apple(AAPL)의 최근 1개월 주가 데이터를 가져와줘.
    2. 두 회사의 종가(Close) 추이를 비교하는 그래프를 그려줘.
    3. 그래프는 'stock_price_comparison.png'로 저장하고 작업이 끝나면 TERMINATE라고 말해줘.
    """
)
