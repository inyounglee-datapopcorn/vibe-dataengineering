# 🦙 LlamaIndex: 데이터와 LLM을 연결하는 최강자

> **강의 목표**: "우리 회사 PDF가 수천 장인데, 이걸 어떻게 AI에게 읽히죠?"라는 질문에 대한 가장 강력한 해답인 **LlamaIndex**를 배웁니다. 데이터를 단순히 보여주는 것을 넘어, AI가 이해하기 좋은 구조(Index)로 만들고 검색(RAG)하는 기술을 마스터합니다.
> 🔗 **공식 문서**: [LlamaIndex Docs](https://docs.llamaindex.ai/)

---

## 1. LlamaIndex란? (The Connector for LLM)

### 💡 한 줄 요약
**"다양한 데이터(PDF, Notion, Slack 등)를 LLM에 연결하여 검색하고 답변하게 만드는 데이터 프레임워크"**

### 🧩 LangChain과의 차이점
- **LangChain**: AI의 '행동(Action)'과 '워크플로우(Chain)' 설계에 강점.
- **LlamaIndex**: AI의 '지식(Data)'과 '검색(RAG)' 효율화에 특화.
> **💡 실무 조합**: 복잡한 에이전트 로직은 LangChain/LangGraph로, 방대한 데이터 처리와 검색은 LlamaIndex로 담당하게 설계하는 경우가 많습니다.

---

## 2. 핵심 개념 (Core Concepts)

### ① LlamaHub & Data Connectors (Reader)
세상의 모든 데이터를 읽어옵니다.
- PDF, API, 데이터베이스, 심지어 Notion이나 Slack 메시지도 클릭 몇 번으로 가져올 수 있습니다.

### ② Indices (Index - 지식의 저장소)
데이터를 AI가 찾기 쉬운 형태(Vector)로 바꿉니다.
- **VectorStoreIndex**: 가장 많이 쓰이는 방식. 의미 기반 검색을 위해 데이터를 수치화(Embedding)하여 저장합니다.

### ③ Query Engine (Query)
사용자의 질문을 받아 답변을 생성합니다.
- 단순히 답변을 주는 것을 넘어, "어떤 문서에서 가져왔는지(Source Node)"를 알려줌으로써 답변의 신빙성을 높입니다.

---

## 3. [심화] VectorDB & VectorStore 이해하기

RAG 시스템의 성능은 "얼마나 질문과 관련된 정보를 잘 찾아오느냐"에 달려 있고, 그 핵심이 바로 벡터 저장소입니다.

### 🧬 무엇이 다른가요?
| 구분 | 일반 DB (SQL) | Vector DB |
| :--- | :--- | :--- |
| **저장 방식** | 텍스트, 숫자 (정형 데이터) | **Vector (수치화된 의미)** |
| **검색 방식** | 키워드 매칭 (정확도) | **유사도 검색 (의미적 거리)** |
| **비유** | "이름이 '김철수'인 사람 찾아줘" | "이 주제와 **가장 비슷한** 내용 찾아줘" |

### 🛠️ 주요 종류 (Toolbox)
*   **파일 기반 (VectorStore)**: 서버 개발 시 로컬에서 가볍게 쓸 때 좋습니다. 
    *   예: `Chroma`, `FAISS`
*   **매니지드 서비스 (VectorDB)**: 대규모 트래픽이나 클라우드 환경에서 안정적으로 운영할 때 씁니다.
    *   예: `Pinecone`, `Milvus`, `Weaviate`

### 🚀 LlamaIndex에서의 역할
LlamaIndex는 로컬 폴더의 문서를 읽어서(Reader) 위와 같은 VectorStore에 예쁘게 저장(Index)해주는 역할을 합니다. 덕분에 우리는 복잡한 수학적 계산 없이도 **"의미 기반 검색"** 기능을 구현할 수 있습니다.

---

---

## 3. [실습] Hello RAG: 로컬 문서로 대화하기

로컬 폴더에 있는 파일을 읽어서 나만의 지식 베이스를 만들어 봅니다.

### 🛠️ 준비 단계
```bash
pip install llama-index llama-index-llms-openai
```

### 📝 실습 코드 예시
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os

# 1. 데이터 로드 (data 폴더 내의 모든 파일 읽기)
documents = SimpleDirectoryReader("./data").load_data()

# 2. 인덱스 생성 (데이터를 학습 가능한 벡터 형태로 변환)
index = VectorStoreIndex.from_documents(documents)

# 3. 쿼리 엔진 생성 및 질문
query_engine = index.as_query_engine()
response = query_engine.query("이 문서의 핵심 내용을 요약해줘.")
print(response)
```

---

## 4. 실전 활용 시나리오

- **사내 지식 베이스**: 입사 매뉴얼, 기술 개발 문서(Wiki)를 연결한 Q&A 봇.
- **법률/금융 문서 분석**: 수많은 판례나 리서치 보고서를 분석하여 요약 및 대조.
- **개인용 제2의 뇌**: 내가 메모한 Notion 데이터나 일기를 연결해 "작년 9월에 내가 계획한 게 뭐였지?" 물어보기.

---

## 5. 채용 시장에서의 위상

- **RAG 전문가 필수**: "RAG(검색 증강 생성) 최적화 경험" 파트에서 LlamaIndex 숙련도는 매우 높게 평가받습니다.
- **데이터 엔지니어링 역량**: 단순히 모델을 돌리는 게 아니라, **"얼마나 고품질의 데이터를 뽑아서 AI에게 먹이느냐"**가 관건인 현상황에서 LlamaIndex는 가속 페달 역할을 합니다.
