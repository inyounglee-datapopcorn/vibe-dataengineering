# 초보자를 위한 dbt 기초 프로젝트: 쇼핑몰 매출 분석하기 🛍️

이 프로젝트는 SQL만 알면 누구나 데이터 파이프라인을 구축할 수 있게 해주는 **dbt(data build tool)**의 핵심 사용법을 익히는 입문 프로젝트입니다.

## 🎯 프로젝트 목표
**"지저분한 원본 주문 데이터를 깔끔한 매출 통계 테이블로 변환하자!"**
1.  **Seed**: CSV 파일을 DB 테이블로 올리기
2.  **Model**: SQL로 데이터 변환하기 (Staging -> Mart)
3.  **Test**: 데이터 숫자가 맞는지 검증하기
4.  **Docs**: 데이터 계보(Lineage) 확인하기

---

## 🏗️ 1단계: 환경 준비 (Setup)
우리는 2일차에 만든 **Supabase(PostgreSQL)**를 그대로 사용합니다.

```bash
# 1. dbt-postgres 설치
pip install dbt-postgres

# 2. 프로젝트 초기화 (이름: my_shop_dbt)
dbt init my_shop_dbt
cd my_shop_dbt
```

`~/.dbt/profiles.yml` 파일에 Supabase 접속 정보를 설정합니다. (비밀번호 보안 주의!)

---

## 🌱 2단계: 데이터 준비 (Seed)
원본 데이터를 직접 넣지 않고, CSV 파일을 활용해 봅니다.
`seeds/raw_orders.csv` 파일을 만들고 아래 내용을 넣습니다.

```csv
order_id,customer_id,order_date,status,amount
1,101,2024-01-01,completed,100
2,102,2024-01-01,completed,150
3,101,2024-01-02,returned,100
4,103,2024-01-03,completed,200
```

그다음 터미널에서 명령어를 실행하면 DB에 테이블이 생깁니다!
```bash
dbt seed
```

---

## 🧑‍💻 3단계: 데이터 모델링 (Models)

### 1) Staging: 원본 데이터 다듬기
`models/stg_orders.sql` 파일을 만듭니다. 반품된 건(`returned`)을 제외합니다.

```sql
with source as (
    select * from {{ ref('raw_orders') }}
)
select
    order_id,
    customer_id,
    order_date,
    amount
from source
where status = 'completed'
```

### 2) Mart: 최종 매출 분석 테이블 만들기
`models/daily_revenue.sql` 파일을 만듭니다. 날짜별 매출을 합산합니다.

```sql
with orders as (
    select * from {{ ref('stg_orders') }}
)
select
    order_date,
    sum(amount) as total_revenue,
    count(order_id) as order_count
from orders
group by 1
```

---

## 🚀 4단계: 실행 및 검증
이제 우리가 작성한 SQL을 DB에서 실행하도록 시킵니다.

```bash
# 1. 모델 실행 (DB에 테이블 생성)
dbt run

# 2. 데이터 품질 테스트 (order_id가 중복되진 않았는지 등)
dbt test

# 3. 문서 및 계보(Lineage) 생성
dbt docs generate
dbt docs serve
```

---

## ✅ 완료 포인트
*   Supabase 대시보드에서 `daily_revenue` 테이블이 생성되었나요?
*   `dbt docs serve`를 켰을 때, `raw -> stg -> daily_revenue`로 이어지는 화살표(계보)가 보이나요?

축하합니다! 여러분은 방금 **애널리틱스 엔지니어(Analytics Engineer)**들이 데이터를 요리하는 가장 표준적인 방법을 마스터하셨습니다. 🥂
