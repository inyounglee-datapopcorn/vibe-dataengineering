"""
서울 지하철 실시간 현황 대시보드
"""
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime, timedelta
from database import get_supabase_client

load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="서울 지하철 현황",
    page_icon="🚇",
    layout="wide"
)

# Supabase 연결
@st.cache_resource
def get_client():
    return get_supabase_client()

supabase = get_client()

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
try:
    df = load_recent_data(time_range)
except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
    st.stop()

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
    
    if not df.empty:
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
    
    if not df.empty:
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
