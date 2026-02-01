# 🦜 LangChain & LangGraph: AI 앱 개발의 표준

> **강의 목표**: "LLM으로 애플리케이션을 만들려면 뭐부터 해야 하죠?"라는 질문에 대한 정답인 **LangChain**과, 차세대 표준인 **LangGraph**를 배웁니다. 단순한 챗봇을 넘어, **기억(Memory)**과 **도구(Tool)**를 사용하는 똑똑한 에이전트를 설계해 봅니다.
> 🔗 **공식 문서**: [LangChain Docs](https://python.langchain.com/docs/introduction/) | [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

---

## 1. LangChain이란? (The "OS" of LLM Apps)

### 💡 한 줄 요약
**"거대언어모델(LLM)을 활용한 애플리케이션 개발을 위한 표준 프레임워크"**

### 🧩 왜 필요한가요?
LLM(GPT-4 등) 자체는 그냥 "텍스트 생성기"일 뿐입니다. 이를 실제 서비스로 만들려면 수많은 부가 기능이 필요합니다.
- **Prompt**: 질문을 예쁘게 포장해서 던져줘야 함.
- **Memory**: 이전 대화 내용을 기억해야 함.
- **RAG**: 우리 회사 매뉴얼(PDF)을 읽고 대답해야 함.

LangChain은 이 모든 기능을 **레고 블록(Component)**처럼 제공합니다.

---

## 2. 핵심 개념 (Core Components)

### ① Chains (체인)
여러 작업을 사슬처럼 연결합니다.
- 예: `질문 받기` -> `프롬프트 수정` -> `LLM 호출` -> `답변 다듬기`
- **LCEL (LangChain Expression Language)**: `prompt | model | output_parser` 형태의 파이프라인 문법을 사용합니다.

### ② Prompts (프롬프트)
LLM에게 "너는 친절한 고객 상담원이야" 같은 역할을 부여하거나, 질문 형식을 지정합니다.
- `PromptTemplate`: 변수(`{question}`)만 바꾸면 재사용 가능한 템플릿.

### ③ Retrievers (검색기 - RAG)
Vector DB(예: Chroma, Pinecone)에서 내 질문과 관련된 문서를 찾아오는 녀석입니다. **RAG의 핵심**입니다.

---

## 3. [심화] LangGraph: 차세대 에이전트 표준

### 🔄 Chain에서 Graph로
LangChain의 `Chain`은 **단방향(일직선)**이었습니다. 하지만 복잡한 에이전트는 "생각해보고, 틀리면 다시 검색해" 같은 **순환(Loop)**이 필요합니다.

### 🕸️ LangGraph의 특징
- **Stateful (상태 유지)**: 에이전트가 현재 어떤 단계(검색 중? 답변 중?)인지 기억합니다.
- **Cyclic (순환)**: 결과가 마음에 안 들면 이전 단계로 되돌아가는 루프를 만들 수 있습니다.
- **Human-in-the-loop**: 에이전트가 뭔가 중요한 결정을 할 때 "사람에게 승인 요청"을 보낼 수 있습니다.

> **💡 실무 포인트**: 2025년 현재, 단순한 챗봇은 LangChain으로, 복잡한 업무 자동화 에이전트는 **LangGraph**로 개발하는 추세입니다.

---

## 4. [실습] LangChain 핸즈온 가이드 (Hands-on Lab)

실제 코드를 돌려보며 에이전트의 동작 원리를 이해해 봅니다.

### 🛠️ 준비 단계 (Setup)

1.  **가상환경 및 라이브러리 설치**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install langchain langchain-openai langchain-community langchainhub tavily-python
    ```

2.  **API 키 설정 (환경 변수)**
    ```bash
    export OPENAI_API_KEY="your_openai_key"
    export TAVILY_API_KEY="your_tavily_key" # 검색 기능을 쓸 때 필요
    ```

### 📝 실습 미션 (Missions)

#### 미션 1: 나만의 전문 챗봇 (Basic LCEL)
프롬프트와 모델을 연결하여 특정 분야의 전문가 챗봇을 만듭니다.
- **실행 파일**: [lab_langchain_agent.py](./lab_langchain_agent.py)의 `run_basic_chain()` 함수 참고.
- **포인트**: `|` (파이프) 기호를 사용하여 데이터가 모델로 흘러가는 구조를 이해합니다.

#### 미션 2: 인터넷 검색 에이전트 (Agent with Tools)
AI가 스스로 필요할 때 구글 검색을 하고 답을 찾게 합니다.
- **실행 파일**: [lab_langchain_agent.py](./lab_langchain_agent.py)의 `run_searching_agent()` 함수 참고.
- **포인트**: AI에게 `Search Tool`이라는 무기를 쥐여줬을 때, AI가 스스로 판단하여 도구를 호출하는지 확인하세요.

#### 미션 3: LangGraph 체험 (Challenge)
에이전트에게 "답변이 틀리면 다시 시도해"라는 루프를 만들어 봅니다. (LangGraph 공식 문서의 'Quickstart' 참고)
- **핵심**: 단순한 '체인'을 넘어 복잡한 '상태(State)'를 관리하는 그래프 구조를 구상해 봅니다.

---

## 5. 채용 시장에서의 위상

- **필수 스택**: JD(채용 공고)에 "LangChain 경험"은 거의 기본값으로 박혀 있습니다.
- **우대 사항**: "LangGraph를 활용한 Multi-Agent 구축 경험"이 있다면 연봉 협상에서 유리한 고지를 점할 수 있습니다.
- **포트폴리오 Tip**: 단순히 "튜토리얼 따라 해봤어요"보다는, **"LangGraph로 여행 계획 짜주는 에이전트를 만들었는데, 날씨 API가 에러 나면 자동으로 재시도하는 로직을 넣었어요"**가 훨씬 강력합니다.
