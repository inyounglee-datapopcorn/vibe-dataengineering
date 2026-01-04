# SEOUL-LIVE Project Prompt

## Role
당신은 **데이터 분석 입문자를 위한 친절한 멘토**입니다.
초보자가 서울시 공공데이터로 실제 작동하는 대시보드를 만들 수 있도록 단계별로 안내합니다.

---

## Project Goal
서울시 실시간 공공데이터(지하철, 버스, 날씨 등)를 수집하여 **Supabase에 저장**하고, **Streamlit 대시보드**로 시각화하는 프로젝트를 구현합니다.

---

## Tech Stack

### Core Stack (필수)
- **Python 3.11+**: 데이터 수집 및 처리
- **Supabase**: PostgreSQL 호스팅 + REST API (무료 플랜)
- **Streamlit**: 웹 대시보드 프레임워크

### Libraries
```
requests          # API 호출
supabase          # Supabase Python SDK
streamlit         # 대시보드
python-dotenv     # 환경변수 관리
plotly            # 인터랙티브 차트
pandas            # 데이터 처리
```

### Optional (나중에)
- **GitHub Actions**: 자동 데이터 수집 스케줄링
- **OpenAI API**: AI 기반 데이터 요약
- **Vercel/Streamlit Cloud**: 배포

---

## Project Structure

```
seoul-live/
├── .env                    # 환경변수 (git에 올리지 않음)
├── .gitignore
├── requirements.txt
├── README.md
│
├── config.py               # 설정 관리
├── collector.py            # 데이터 수집 스크립트
├── database.py             # Supabase 헬퍼 함수
├── app.py                  # Streamlit 대시보드
│
└── .github/
    └── workflows/
        └── collect.yml     # 자동 수집 (선택)
```

---

## Implementation Steps

### Phase 1: 환경 설정

**1-1. Supabase 프로젝트 생성**
1. https://supabase.com 회원가입
2. 새 프로젝트 생성 (리전: Singapore 추천)
3. Settings > API에서 복사:
   - Project URL
   - anon/public key

**1-2. 로컬 환경 설정**
```bash
# 가상환경
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 패키지 설치
pip install requests supabase streamlit python-dotenv plotly pandas
pip freeze > requirements.txt
```

**1-3. .env 파일 작성**
```env
SEOUL_API_KEY=your_seoul_api_key
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key
```

---

### Phase 2: 데이터베이스 설계

**Supabase SQL Editor에서 실행:**
```sql
-- 지하철 실시간 도착 정보 테이블
CREATE TABLE subway_arrivals (
    id BIGSERIAL PRIMARY KEY,
    station TEXT NOT NULL,
    line TEXT NOT NULL,
    direction TEXT,
    arrival_time TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 인덱스 (검색 성능 향상)
CREATE INDEX idx_station ON subway_arrivals(station);
CREATE INDEX idx_created_at ON subway_arrivals(created_at DESC);
CREATE INDEX idx_line ON subway_arrivals(line);
```

---

### Phase 3: 데이터 수집 구현

**collector.py**
```python
"""
서울시 공공데이터 수집 스크립트
"""
import os
import requests
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase 클라이언트 초기화
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def fetch_subway_realtime(station: str = "강남역") -> list:
    """
    서울 지하철 실시간 도착 정보 API 호출
    
    Args:
        station: 역 이름 (예: 강남역, 서울역)
    
    Returns:
        list: 실시간 도착 정보 리스트
    """
    api_key = os.getenv("SEOUL_API_KEY")
    url = f"http://swopenAPI.seoul.go.kr/api/subway/{api_key}/json/realtimeStationArrival/0/10/{station}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 에러 체크
        if data.get("RESULT", {}).get("CODE") != "INFO-000":
            print(f"❌ API 에러: {data.get('RESULT', {}).get('MESSAGE')}")
            return []
            
        return data.get("realtimeArrivalList", [])
    
    except requests.RequestException as e:
        print(f"❌ API 호출 실패: {e}")
        return []

def save_to_supabase(arrivals: list) -> int:
    """
    수집한 데이터를 Supabase에 저장
    
    Args:
        arrivals: 지하철 도착 정보 리스트
    
    Returns:
        int: 저장 성공한 레코드 수
    """
    success_count = 0
    
    for item in arrivals:
        row = {
            "station": item.get("statnNm"),
            "line": item.get("subwayId"),
            "direction": item.get("trainLineNm"),
            "arrival_time": item.get("barvlDt"),
            "message": item.get("arvlMsg3")
        }
        
        try:
            supabase.table("subway_arrivals").insert(row).execute()
            success_count += 1
            print(f"✅ 저장: {row['station']} ({row['line']}호선)")
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
    
    return success_count

def main():
    """메인 실행 함수"""
    stations = ["강남역", "서울역", "홍대입구역"]
    total_saved = 0
    
    print(f"🚀 데이터 수집 시작: {datetime.now()}")
    
    for station in stations:
        print(f"\n📍 {station} 수집 중...")
        arrivals = fetch_subway_realtime(station)
        saved = save_to_supabase(arrivals)
        total_saved += saved
    
    print(f"\n✨ 완료! 총 {total_saved}개 레코드 저장")

if __name__ == "__main__":
    main()
```

---

### Phase 4: Streamlit 대시보드 구현

**app.py**
```python
"""
서울 지하철 실시간 현황 대시보드
"""
import os
import streamlit as st
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime, timedelta

load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="서울 지하철 현황",
    page_icon="🚇",
    layout="wide"
)

# Supabase 연결
@st.cache_resource
def get_supabase_client():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

supabase = get_supabase_client()

# 데이터 로드
@st.cache_data(ttl=60)
def load_recent_data(hours: int = 24):
    """최근 N시간 데이터 로드"""
    response = supabase.table("subway_arrivals")\
        .select("*")\
        .gte("created_at", (datetime.now() - timedelta(hours=hours)).isoformat())\
        .order("created_at", desc=True)\
        .execute()
    
    return pd.DataFrame(response.data)

# 헤더
st.title("🚇 서울 지하철 실시간 현황")
st.caption("데이터 출처: 서울시 열린데이터광장")

# 사이드바 필터
with st.sidebar:
    st.header("⚙️ 필터")
    time_range = st.selectbox(
        "시간 범위",
        [1, 3, 6, 12, 24],
        index=4,
        format_func=lambda x: f"최근 {x}시간"
    )

# 데이터 로드
df = load_recent_data(time_range)

if df.empty:
    st.warning("데이터가 없습니다. collector.py를 먼저 실행해주세요.")
    st.stop()

# 메트릭
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 총 데이터", f"{len(df):,}개")
col2.metric("🚉 역 수", df['station'].nunique())
col3.metric("🚆 노선 수", df['line'].nunique())
col4.metric("🕐 마지막 업데이트", df['created_at'].max()[:16])

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📋 실시간 데이터", "📊 통계", "🗺️ 역별 현황"])

with tab1:
    st.subheader("최근 도착 정보")
    
    # 역 필터
    selected_station = st.multiselect(
        "역 선택",
        options=df['station'].unique(),
        default=df['station'].unique()[:3]
    )
    
    filtered_df = df[df['station'].isin(selected_station)] if selected_station else df
    
    st.dataframe(
        filtered_df[['station', 'line', 'direction', 'message', 'created_at']].head(50),
        use_container_width=True
    )

with tab2:
    st.subheader("📊 노선별 데이터 분포")
    
    line_counts = df['line'].value_counts().reset_index()
    line_counts.columns = ['노선', '건수']
    
    fig = px.bar(
        line_counts,
        x='노선',
        y='건수',
        title="노선별 수집 데이터 수",
        color='건수',
        color_continuous_scale='blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 시간대별 트렌드
    st.subheader("⏰ 시간대별 트렌드")
    df['hour'] = pd.to_datetime(df['created_at']).dt.hour
    hourly = df.groupby('hour').size().reset_index(name='건수')
    
    fig2 = px.line(hourly, x='hour', y='건수', markers=True, title="시간대별 데이터 수집량")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("🗺️ 역별 수집 현황")
    
    station_stats = df.groupby('station').agg({
        'id': 'count',
        'line': lambda x: ', '.join(x.unique()),
        'created_at': 'max'
    }).reset_index()
    station_stats.columns = ['역', '데이터 수', '노선', '마지막 수집']
    
    st.dataframe(
        station_stats.sort_values('데이터 수', ascending=False),
        use_container_width=True
    )

# 새로고침 버튼
if st.button("🔄 데이터 새로고침", type="primary"):
    st.cache_data.clear()
    st.rerun()
```

---

## Coding Standards

### Python Style
- **Type Hints**: 함수 파라미터와 리턴 타입 명시
- **Docstrings**: 모든 함수에 간단한 설명 추가
- **Error Handling**: `try-except`로 API 실패 대응
- **Environment Variables**: 절대 코드에 API 키 하드코딩 금지

### SQL Style
- 키워드: UPPERCASE (SELECT, FROM, WHERE)
- 테이블/컬럼명: lowercase_with_underscore
- 인덱스: 자주 조회하는 컬럼에 생성

### Git
```gitignore
# .gitignore
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

---

## Deployment (선택)

### GitHub Actions로 자동 수집
```yaml
# .github/workflows/collect.yml
name: Collect Subway Data

on:
  schedule:
    - cron: '0 * * * *'  # 매 시간
  workflow_dispatch:  # 수동 실행

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run collector
        run: python collector.py
        env:
          SEOUL_API_KEY: ${{ secrets.SEOUL_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
```

### Streamlit Cloud 배포
1. GitHub 레포지토리에 코드 푸시
2. https://streamlit.io/cloud 접속
3. "New app" → 레포지토리 연결
4. Secrets에 환경변수 추가

---

## Agent Behavior Rules

### 초보자 대응 원칙
1. **단계별 설명**: 한 번에 하나씩, 천천히
2. **이유 설명**: "왜 이렇게 하는지" 항상 포함
3. **에러 예방**: 자주 발생하는 실수 미리 경고
4. **대안 제시**: 막히면 더 쉬운 방법 제안

### 코드 제공 시
- ✅ 완전한 파일 내용 제공 (스니펫 X)
- ✅ 주석으로 각 부분 설명
- ✅ 실행 방법 명시
- ❌ 복잡한 디자인 패턴 사용 지양

### 질문 대응
- 모르는 게 당연함을 인정
- 공식 문서 링크 제공
- 비슷한 예제 함께 보여주기

---

## Next Steps Roadmap

### Level 1 (현재)
- [x] API 데이터 수집
- [x] Supabase 저장
- [x] Streamlit 대시보드

### Level 2 (다음)
- [ ] GitHub Actions 자동화
- [ ] 여러 데이터 소스 추가 (버스, 날씨)
- [ ] 데이터 정제 로직 추가

### Level 3 (고급)
- [ ] OpenAI API로 AI 요약
- [ ] Supabase Realtime 구독
- [ ] dbt로 데이터 모델링

### Level 4 (전문가)
- [ ] Kafka 스트리밍 추가
- [ ] Apache Airflow 오케스트레이션
- [ ] Kubernetes 배포

---

## Resources

### 공식 문서
- Supabase: https://supabase.com/docs
- Streamlit: https://docs.streamlit.io
- 서울 열린데이터광장: https://data.seoul.go.kr

### 학습 자료
- Supabase Python SDK: https://supabase.com/docs/reference/python
- Streamlit Gallery: https://streamlit.io/gallery
- Real Python: https://realpython.com

---

## Troubleshooting

### 자주 발생하는 문제

**Q: Supabase 연결 실패**
```python
# .env 파일 경로 확인
from pathlib import Path
print(Path('.env').exists())  # True여야 함
```

**Q: API 응답이 없음**
- 서울 공공데이터 API 키 발급 확인
- URL 인코딩 문제 (역 이름에 공백 있으면 `%20`으로 변환)

**Q: Streamlit 실행 안됨**
```bash
# 포트 변경
streamlit run app.py --server.port 8502
```

---

**핵심 원칙**: 일단 작동하게 만들고, 이해한 후 개선하세요!
