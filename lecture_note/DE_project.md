# 🚖 실습 프로젝트: Uber Data Analytics (Beginner Ver.)

이 실습은 Darshil Parmar의 유명한 "Uber Data Analytics" 프로젝트를 비전공자 초보자가 **6시간 내에 클라우드 비용 부담 없이 로컬 환경에서 완료**할 수 있도록 재구성한 가이드입니다.

---

## 🎯 학습 목표
1. **데이터 모델링(Dimensional Modeling)** 이해: 지저분한 하나의 표를 여러 개의 의미 있는 표(Fact/Dimension)로 나누는 이유를 배웁니다.
2. **E2E 파이프라인 경험**: `데이터 로드 -> 가공(Transformation) -> 시각화(Dashboard)`의 흐름을 직접 구현합니다.

---

## ⌚ 타임라인 (총 6시간 코스)

### [1교시] 개념 잡기 & 환경 세팅 (1시간)
- **영상 시청**: YouTube에서 **"Darshil Parmar Uber Data Analytics"** 검색 및 시청. (코딩보다 '데이터 모델링' 개념에 집중!)
- **환경 구축**: Python 설치 및 필요한 라이브러리(`pandas`, `streamlit`, `plotly`) 설치.
- **데이터 준비**: NYC TLC Trip Record Data 샘플(CSV) 준비.

### [2교시] 데이터 모델링 실습 (2시간)
- **Pandas 활용**: 원본 CSV 파일을 불러와서 Darshil이 제안한 구조대로 데이터 쪼개기.
  - `datetime_dim` (날짜/시간)
  - `passenger_count_dim` (승객 수)
  - `fact_table` (중심 테이블) 생성
- **중요**: 왜 테이블을 나누는지(정규화) 스스로 설명해보기.

### [3교시] 데이터 통합 및 분석 (1시간)
- **Merge 작업**: 쪼개진 테이블들을 다시 하나로 합쳐서(Join) 분석용 데이터셋(Analytical Table) 만들기.
- **기초 통계**: 시간대별, 요일별 평균 요금 및 탑승 횟수 계산.

### [4교시] 대시보드 시각화 (2시간)
- **Streamlit 사용**: `app.py` 작성.
-  차트 구현:
   - 시간대별 택시 탑승 현황 (Bar Chart)
   - 요일별 매출 분석
   - 지도 위에 탑승 위치 찍어보기 (선택 사항)
- **최종 점검**: 누구나 이해할 수 있는 리포트 형태로 구성.

---

## 💻 프로젝트 착수를 위한 AGENT 가이드

이 내용을 AI(Antigravity 등)에게 전달하여 프로젝트를 시작하세요.

### 📄 `AGENT.md` (Uber Project Ver.)
```markdown
# AGENT.md - Uber Data Analytics (Beginner Local Version)

## 1. Project Context
**Goal:** Build a local data pipeline to analyze Uber trip data.
**Reference:** Based on Darshil Parmar's "Uber Data Analytics" project but adapted for a local environment (No Cloud/GCP for now).
**User Level:** Beginner. Needs clear explanations.

## 2. Tech Stack
- **Language:** Python 3.9+
- **Data Processing:** Pandas (for data modeling).
- **Visualization:** Streamlit.
- **Input:** `uber_data.csv` (Flat CSV file).
- **Output:** A Streamlit dashboard showing trip statistics.

## 3. Key Requirement: Data Modeling (Important!)
You must implement the **Dimensional Modeling** logic demonstrated by Darshil Parmar.
Instead of using one big DataFrame, split the data into:
1.  `datetime_dim`: pickup_hour, pickup_day, pickup_month, pickup_weekday.
2.  `passenger_count_dim`: passenger_count.
3.  `trip_distance_dim`: trip_distance.
4.  `rate_code_dim`: rate_code_name.
5.  `fact_table`: The central table connecting all dimensions via ID columns.

## 4. Coding Tasks
1.  **Load Data:** Read csv using Pandas.
2.  **Transform:** Create the dimension tables and the fact table exactly as defined above.
3.  **Merge:** For the final visualization, join the tables back together to create a wide "Analytical Table".
4.  **Visualize:** Use Streamlit to show a bar chart of "Trips by Hour".

## 5. Agent Persona
- Be a helpful mentor.
- Explain *why* we are splitting the tables (Normalization).
- Provide the full `app.py` code that handles both processing and visualization.
```

---

## 🚀 다음 단계 (Next Action)

준비가 되었다면 AI에게 다음과 같이 요청하세요:

> **"위 AGENT.md 내용을 바탕으로, `uber_data.csv` 파일을 읽어서 데이터 모델링을 수행하고 차트를 그려주는 `app.py` 전체 코드를 작성해 줘. 샘플 데이터는 코드 내에서 생성하거나 Kaggle 링크를 알려줘."**
