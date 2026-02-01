import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. 환경 변수 로드 (.env 파일에서 API 키를 가져옵니다)
load_dotenv()

def run_llamaindex_rag():
    print("\n--- LlamaIndex RAG Workshop Start ---")
    
    # 2. 데이터 준비 (data 폴더가 없으면 생성하고 샘플 텍스트 저장)
    if not os.path.exists("./data"):
        os.makedirs("./data")
        with open("./data/workshop_info.txt", "w", encoding="utf-8") as f:
            f.write("본 워크숍은 2026년 최신 AI 에이전트 개발 트렌드를 다룹니다.\n")
            f.write("강사는 'Popcorn'이며, 주요 프레임워크는 LangChain, AutoGen, CrewAI, LlamaIndex입니다.")
    
    try:
        # 3. 데이터 로드 (Reader)
        print("1) 데이터를 로드하는 중...")
        documents = SimpleDirectoryReader("./data").load_data()
        
        # 4. 인덱스 생성 (Index)
        print("2) 벡터 인덱스를 생성하는 중 (Embedding)...")
        index = VectorStoreIndex.from_documents(documents)
        
        # 5. 쿼리 엔진 생성 (Query Engine)
        query_engine = index.as_query_engine()
        
        # 6. 질문 및 답변
        print("3) AI에게 질문 중...")
        user_question = "이 워크숍의 주요 프레임워크는 어떤 것들이 있어?"
        response = query_engine.query(user_question)
        
        print(f"\nQ: {user_question}")
        print(f"A: {response}")
        
    except Exception as e:
        print(f"에러 발생: {e}. (.env 파일에 OPENAI_API_KEY가 설정되어 있는지 확인하세요.)")

if __name__ == "__main__":
    run_llamaindex_rag()
    print("\n--- Mission Completed ---")
