# 🚣‍♀️ CrewAI: 역할극 기반의 AI 팀 빌딩

> **강의 목표**: 혼자 일하는 AI가 아니라, **"여러 명의 AI가 협업하는(Multi-Agent)"** 시스템을 만듭니다. 마치 회사에서 팀장님이 업무를 지시하고 팀원들이 협업하듯, 직관적인 코드로 나만의 AI 팀(Crew)을 조직해 봅니다.
> 🔗 **공식 문서**: [CrewAI Docs](https://docs.crewai.com/)

---

## 1. CrewAI란? (Role-Based Team)

### 💡 한 줄 요약
**"개발자, 기획자, 디자이너처럼 '역할(Role)'을 가진 AI 에이전트들이 협업하는 프레임워크"**

### 🧩 왜 필요한가요?
GPT-4 혼자서 코딩도 하고, 글도 쓰고, 번역도 하면 헷갈려(Hallucination) 합니다.
**"전문가 한 명에게 하나씩 시키자"**는 것이 CrewAI의 철학입니다.
- **Agent A (Researcher)**: 자료 조사만 해.
- **Agent B (Writer)**: 조사된 자료로 글만 써.
- **Agent C (Manager)**: 둘이 제대로 하는지 감시해.

---

## 2. 핵심 개념 (Core Components)

### ① Agent (직원)
특정 기술과 목표를 가진 팀원입니다.
- `Role`: 직책 (예: 수석 연구원)
- `Goal`: 목표 (예: 최신 AI 트렌드 조사)
- `Backstory`: 페르소나 (예: "당신은 10년 차 베테랑 연구원입니다...")

### ② Task (업무)
에이전트가 수행해야 할 구체적인 일입니다.
- "2025년 AI 트렌드에 대한 보고서를 작성해라."

### ③ Process (업무 방식)
팀원들이 어떻게 일할지 정합니다.
- **Sequential (순차)**: A가 끝내면 B가 받아서 이어서 함. (가장 많이 씀)
- **Hierarchical (계층)**: 팀장(Manager)이 알아서 일을 분배함.

---

## 3. [실습] CrewAI 핸즈온 가이드 (Hands-on Lab)

개별 에이전트가 아니라, 한 팀의 '운영진'이 되어 워크플로우를 관리해 봅니다.

### 🛠️ 준비 단계 (Setup)

1.  **가상환경 및 통합 패키지 설치**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **환경 변수 설정 (`.env`)**
    - [.env.template](./.env.template) 파일을 복사하여 `.env` 파일을 만듭니다.
    - 파일 안에 본인의 `OPENAI_API_KEY`를 입력하세요.

### 📝 실습 미션 (Missions)

#### 미션 1: 시장 조사 팀 결성 (Market Analysis Team)
연구원과 작가를 한 팀으로 묶어 보고서를 뽑아냅니다.
- **실행 파일**: [lab_crewai_team.py](./lab_crewai_team.py)
- **명령어**: `python lab_crewai_team.py`
- **관람 포인트**: 터미널 로그에서 Researcher가 먼저 일을 끝내고, 그 결과를 Writer가 받아서 글을 쓰는 **"바톤 터치(Sequential Process)"** 과정을 유심히 보세요.

#### 미션 2: 에이전트 추가 및 위임 (Delegation)
더 전문적인 글을 위해 `SEO 전문가` 에이전트를 추가해 보세요.
- `role='SEO Specialist', goal='검색 엔진 최적화 키워드를 고르세요.'` 등의 에이전트를 정의합니다.
- `writer` 에이전트의 `allow_delegation=True` 설정을 통해 Writer가 SEO 전문가에게 키워드를 물어보게 구성할 수 있습니다.

---

## 4. 실무 활용 및 팁

- **너무 많은 에이전트는 독이다**: 오히려 서로 대화하느라 돈과 시간이 많이 듭니다. 최소한의 인원(2~3명)으로 시작하세요.
- **명확한 R&R**: 에이전트의 Role과 Goal을 최대한 구체적으로 써야(Prompt Engineering) 결과가 좋습니다.
- **도구(Tools) 쥐여주기**: `SerperDevTool`(구글 검색) 같은 걸 주면 퀄리티가 훨씬 좋아집니다.

---

## 5. 채용 시장에서의 위상

- **직관성**: 코드가 매우 깔끔해서, 비개발자 출신 기획자나 PM이 프로토타입을 만들 때 가장 선호합니다.
- **비즈니스 자동화**: 고객 상담 -> 분류 -> 담당자 배정 같은 **"정형화된 업무 프로세스"**를 자동화하는 프로젝트에서 많이 쓰입니다.
