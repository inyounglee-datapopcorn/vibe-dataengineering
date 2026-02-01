import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub

# 1. 기본 설정 (API 키가 환경 변수에 설정되어 있어야 합니다)
# os.environ["OPENAI_API_KEY"] = "sk-..."
# os.environ["TAVILY_API_KEY"] = "tvly-..." # 검색 기능을 쓰려면 필요합니다.

# 🚀 Mission 1: 기본 LCEL 체인 (Brain + Role)
def run_basic_chain():
    print("\n--- Mission 1: Basic LCEL Chain ---")
    model = ChatOpenAI(model="gpt-4o")
    prompt = ChatPromptTemplate.from_template("너는 {topic} 전문가야. {question}에 대해 답변해줘.")
    
    # 사슬처럼 연결 (Chain)
    chain = prompt | model | StrOutputParser()
    
    result = chain.invoke({"topic": "전기차", "question": "배터리 수명을 늘리는 방법은?"})
    print(f"AI 답변: {result}")

# 🚀 Mission 2: 도구를 사용하는 에이전트 (Brain + Tool)
def run_searching_agent():
    print("\n--- Mission 2: Tool-using Agent ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # 도구 설정 (인터넷 검색 도구)
    # Tavily API 키가 없다면 DuckDuckGoSearchRun 등으로 대체 가능합니다.
    try:
        tools = [TavilySearchResults(max_results=1)]
        
        # 에이전트 프롬프트 가져오기 (LangChain Hub)
        prompt = hub.pull("hwchase17/openai-functions-agent")
        
        # 에이전트 생성
        agent = create_openai_functions_agent(llm, tools, prompt)
        
        # 에이전트 실행기 생성
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        agent_executor.invoke({"input": "2026년 한국의 AI 시장 전망에 대해 최신 뉴스를 검색해서 알려줘."})
    except Exception as e:
        print(f"에러 발생: {e}. (TAVILY_API_KEY 설정을 확인하세요)")

if __name__ == "__main__":
    run_basic_chain()
    run_searching_agent()
