import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# 1. 환경 변수 로드 (.env 파일을 만들어 키를 넣어주세요)
load_dotenv()

# 🚀 Mission: AI 에이전트 시장 분석 보고서 작성 팀 구성

# 2. 에이전트 정의 (직무 부여)
researcher = Agent(
    role='Market Researcher',
    goal='2026년 글로벌 AI 에이전트 시장의 핵심 트렌드 3가지를 분석하세요.',
    backstory="""당신은 실리콘밸리 벤처캐피털(VC)에서 근무 중인 베테랑 시장 분석가입니다. 
    복잡한 기술 트렌드에서 핵심적인 비즈니스 기회를 포착하는 데 천부적인 재능이 있습니다.""",
    verbose=True,
    allow_delegation=False  # 다른 에이전트에게 일을 떠넘기지 않음
)

writer = Agent(
    role='Tech Reporter',
    goal='분석 보고서를 바탕으로 대중이 이해하기 쉬운 기술 블로그 포스팅을 작성하세요.',
    backstory="""당신은 Wired나 TechCrunch의 선임 에디터입니다. 
    복잡한 기술 내용을 흡입력 있고 설득력 있는 문장으로 변환하는 능력이 탁월합니다.""",
    verbose=True,
    allow_delegation=True  # 필요시 메인 분석가에게 추가 질문 가능
)

# 3. 업무 지시 (Task 설계)
research_task = Task(
    description="""2026년 AI 에이전트 시장 변화에 대한 심층 조사를 수행하세요. 
    특히 OpenAI, Anthropic, Google의 최근 행보를 중심으로 기업들이 왜 '에이전트'에 열광하는지 분석하세요.""",
    expected_output="AI 에이전트 시장의 핵심 트렌드 3가지를 정리한 불렛 포인트 리스트",
    agent=researcher
)

writing_task = Task(
    description="""연구원이 분석한 자료를 바탕으로 블로그 글을 작성하세요. 
    제목은 사람들의 클릭을 유도할 수 있어야 하며, 결론 부분에는 취준생들이 어떤 준비를 해야 하는지 제언을 담으세요.""",
    expected_output="블로그 스타일의 Markdown 형식 포스팅 전문",
    agent=writer
)

# 4. 크루 결성 (팀 빌딩)
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # 순차적 업무 진행
    verbose=True
)

# 5. 실행
print("\n--- CrewAI Workshop Start ---")
result = crew.kickoff()

print("\n\n########################")
print("## FINAL OUTPUT ##")
print("########################\n")
print(result)
