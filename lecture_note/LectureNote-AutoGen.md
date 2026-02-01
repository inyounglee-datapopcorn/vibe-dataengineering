# 🗣️ AutoGen: 대화하고 코딩하는 자율 에이전트

> **강의 목표**: "에이전트끼리 싸우면서(토론하면서) 답을 찾으면 더 정확하지 않을까?"라는 아이디어에서 출발합니다. Microsoft가 만든, **대화(Conversation)**와 **코드 실행(Code Execution)**에 특화된 강력한 프레임워크를 경험해 봅니다.
> 🔗 **공식 문서**: [AutoGen Docs](https://microsoft.github.io/autogen/)

---

## 1. AutoGen이란? (Conversation-First)

### 💡 한 줄 요약
**"에이전트끼리 '대화'를 통해 복잡한 문제를 해결하고, 코드를 직접 짜서 돌려보는 프레임워크"**

### 🧩 왜 필요한가요?
LLM은 수학 계산이나 복잡한 논리에 약합니다. AutoGen은 이 문제를 두 가지로 해결합니다.
1.  **Multi-Agent Conversation**: 한 명이 틀리면 다른 명이 "그거 틀린 것 같은데?"라고 지적하며 고칩니다.
2.  **Code Executions**: "답이 3.5야"라고 찍는 게 아니라, 파이썬 코드를 짜서 실제로 계산해보고 "실행해보니 3.5네"라고 검증합니다.

---

## 2. 핵심 개념 (Core Components)

### ① ConversableAgent (대화형 에이전트)
AutoGen의 모든 에이전트는 서로 대화할 수 있습니다.
- **AssistantAgent**: AI 역할을 하는 녀석. (LLM 사용) 코드를 짜거나 답을 제안합니다.
- **UserProxyAgent**: 사람(User)을 대신하거나, **코드를 실행(Executor)**하는 녀석. AI가 짠 코드를 받아서 내 컴퓨터에서 돌려보고 결과를 알려줍니다.

### ② Conversation Patterns (대화 패턴)
- **Two-Agent Chat**: 둘이서 핑퐁.
- **Group Chat**: 여러 명이 단톡방에서 대화. (Manager가 발언권 조정)

---

## 3. [실습] AutoGen 핸즈온 가이드 (Hands-on Lab)

이 실습을 통해 에이전트가 코드를 짜고 실행하는 과정을 직접 확인해 봅니다.

### 🛠️ 준비 단계 (Setup)

1.  **가상환경 생성 및 라이브러리 설치**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    pip install pyautogen yfinance matplotlib
    ```

2.  **API 키 설정 (`OAI_CONFIG_LIST`)**
    - [OAI_CONFIG_LIST.json.template](./OAI_CONFIG_LIST.json.template) 파일을 복사하여 `OAI_CONFIG_LIST` 파일을 만듭/니다.
    - 본인의 OpenAI API 키를 입력하세요.

### 📝 실습 미션 (Missions)

#### 미션 1: 코드 실행형 에이전트 (Stock Analysis)
AI가 직접 데이터를 수집하고 그래프를 그리게 합니다.
- **실행 파일**: [lab_autogen_stock.py](./lab_autogen_stock.py)
- **명령어**: `python lab_autogen_stock.py`
- **관람 포인트**: 터미널에 `user_proxy (to assistant)` 대화가 오가며 `coding` 폴더 내에 파이썬 파일과 그래프 결과물이 생성되는지 확인하세요.

#### 미션 2: 멀티 에이전트 협업 (Group Chat)
글을 쓰는 에이전트와 검수하는 에이전트를 팀으로 묶어봅니다. (코드 수정 실습)
- 위 `lab_autogen_stock.py`를 복사하여 `ラボ_autogen_team.py`를 만듭니다.
- `Reviewer` 에이전트를 추가하고 `GroupChat` 클래스를 활용해 보세요.

```python
# Group Chat 예시 코드 조각
user_proxy = UserProxyAgent(name="Admin", ...)
writer = AssistantAgent(name="Writer", system_message="블로그 포스트를 작성해.", ...)
reviewer = AssistantAgent(name="Reviewer", system_message="오타와 논리를 검수해.", ...)

groupchat = GroupChat(agents=[user_proxy, writer, reviewer], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
```

> **😲 놀라운 점**:
> 실행하면 AI가 `yfinance` 라이브러리를 써야 한다고 판단하고, 스스로 **pip install** 코드를 짜고, 그래프 그리는 코드를 실행해서 `.png` 파일까지 만들어냅니다.

---

## 4. 실무 활용 및 팁

- **Code Execution의 위험성**: 에이전트가 `rm -rf /`(전체 삭제) 같은 코드를 짜버리면 큰일 납니다. 그래서 실무에서는 반드시 **Docker** 환경(샌드박스) 안에서만 코드를 돌리도록 설정해야 합니다.
- **복잡한 문제 해결**: 수학 문제, 데이터 분석, 크롤링 등 "정답이 있는" 문제나 "실행이 필요한" 문제에 압도적으로 강합니다.

---

## 5. 채용 시장에서의 위상

- **연구/R&D**: 새로운 알고리즘을 테스트하거나 복잡한 문제를 푸는 연구 조직에서 선호합니다.
- **Code Interpreter**: "회사 내부 데이터로 그래프 그려주는 봇"을 만들 때 가장 강력한 후보입니다. (OpenAI의 Code Interpreter 기능을 직접 구현하는 셈)
