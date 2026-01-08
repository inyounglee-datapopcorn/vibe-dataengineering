# 초보자를 위한 Airflow 기초 프로젝트: 비트코인 가격 추적기 🪙

이 프로젝트는 Airflow를 처음 접하는 분들이 **"설치부터 실행까지"** 가장 빠르게 핵심 개념을 익힐 수 있도록 설계된 입문용 가이드입니다.

## 🎯 프로젝트 목표
**"매 10분마다 비트코인 현재 가격을 가져와서 내 파일에 기록하자!"**
이 목표를 달성하며 우리는 다음 3가지를 마스터합니다.
1.  **DAG (Directed Acyclic Graph)**: 작업의 순서를 그림 그리기
2.  **Operator**: 실제로 일을 하는 일꾼 부리기 (PythonOperator)
3.  **Scheduling**: 정해진 시간에 자동으로 실행하기

---

## 🏗️ 1단계: 환경 준비 (Local Setup)
복잡한 도커(Docker) 대신, 파이썬 가상환경에서 가장 가볍게 시작합니다.

```bash
# 1. 가상환경 생성 및 활성화
python -m venv airflow_env
source airflow_env/bin/activate  # Windows: airflow_env\Scripts\activate

# 2. Apache Airflow 설치 (시간이 좀 걸립니다!)
pip install apache-airflow

# 3. Airflow 홈 디렉토리 설정 (현재 폴더로 지정)
export AIRFLOW_HOME=$(pwd)

# 4. DB 초기화 및 사용자 생성
airflow db init
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email admin@example.com
```

---

## 🖼️ 2단계: DAG 설계 (작업 흐름도)
우리의 로봇(Airflow)에게 시킬 일의 순서는 다음과 같습니다.

1.  **시작 (Start)**: "작업을 시작합니다"라고 로그 남기기
2.  **가격 가져오기 (Fetch Price)**: 외부 API에서 비트코인 가격 가져오기
3.  **저장하기 (Save Data)**: 가져온 가격을 `bitcoin_data.csv` 파일에 저장하기
4.  **끝 (End)**: "작업이 완료되었습니다"라고 로그 남기기

**[흐름도]**
`Start` -> `Fetch Price` -> `Save Data` -> `End`

---

## 🧑‍💻 3단계: 코드 작성 (`dags/bitcoin_dag.py`)
아래 코드를 `dags` 폴더 안에 저장합니다.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import csv

# 1. 비트코인 가격을 가져오는 함수 (Task 1)
def fetch_btc_price(**kwargs):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = data['bitcoin']['usd']
    return price

# 2. 가격을 파일에 저장하는 함수 (Task 2)
def save_price(ti):
    # 이전 Task에서 가져온 가격을 꺼냅니다 (XCom 기능)
    price = ti.xcom_pull(task_ids='fetch_price')
    
    with open('bitcoin_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), price])

# 3. DAG 정의 (작업 명세서 - 모든 주요 설정 옵션 포함)
with DAG(
    dag_id='bitcoin_tracker_v1',         # DAG의 고유 ID (파일 내에서 유일해야 함)
    description='비트코인 가격을 추적하고 저장합니다.', # DAG에 대한 설명
    start_date=datetime(2024, 1, 1),     # DAG가 시작되는 시각
    # end_date=datetime(2025, 1, 1),     # DAG가 종료되는 시각 (없으면 무한 반복)
    schedule_interval='*/10 * * * *',    # 실행 주기 (Cron 표현식: 매 10분마다)
    catchup=False,                       # 과거 예약 시간 중 실행되지 않은 작업을 백필(Backfill)할지 여부
    tags=['finance', 'bitcoin', 'kdt'],  # UI에서 필터링을 조절하기 위한 태그
    max_active_runs=1,                   # 동시에 활성화될 수 있는 DAG Run의 최대 합계
    # max_active_tasks=16,               # DAG 내에서 동시에 실행될 수 있는 Task의 최대 개수
    dagrun_timeout=timedelta(hours=),   # DAG Run이 성공으로 끝나야 하는 최대 시간
    default_args={                       # 하위 작업(Task)들에 공통으로 적용될 기본 설정들
        'owner': 'airflow',              # 소유자 정보
        'email' : ['all@datapopcorn.ai', '1@datapopcorn.ai', '2@datapopcorn.ai'],
        'depends_on_past': False,        # 이전 날짜의 Task가 성공해야만 현재 Task를 실행할지 여부
        'retries': 1,                    # 실패 시 재시도 횟수
        'retry_delay': timedelta(minutes=5), # 재시도 간격
        'email_on_failure': True,       # 실패 시 이메일 알림 여부
        'on_failure_callback': None,   # 실패 시 실행할 함수 (Slack)
    }
) as dag:

    # Task 정의
    fetch_task = PythonOperator(
        task_id='fetch_task',
        python_callable=fetch_task
    )

    save_task = PythonOperator(
        task_id='save_data',
        python_callable=save_price
    )

    # 순서 연결
    fetch_task >> save_task
```

---

## 🚀 4단계: 실행 및 확인
Airflow는 두 개의 심장(서비스)을 켜야 합니다.

1.  **Scheduler**: 알람 시계처럼 시간을 감시하고 작업을 지시함
    ```bash
    airflow scheduler
    ```
2.  **Webserver**: 우리가 눈으로 보고 제어하는 웹사이트
    ```bash
    airflow webserver -p 8080
    ```

이제 브라우저에서 `localhost:8080`으로 접속하면, 우리가 만든 `bitcoin_tracker_v1`이 보일 것입니다! 스위치를 **ON**으로 켜보세요.

---

## ✅ 완료 포인트
*   10분 뒤에 프로젝트 폴더에 `bitcoin_data.csv` 파일이 생겼나요?
*   파일 안에 시간과 비트코인 가격이 적혀있나요?

축하합니다! 여러분은 방금 전 세계 데이터 엔지니어들이 쓰는 도구로 첫 번째 **자동화 파이프라인**을 만드셨습니다. 🎉
