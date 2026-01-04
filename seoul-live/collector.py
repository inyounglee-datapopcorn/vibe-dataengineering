"""
서울시 공공데이터 수집 스크립트
"""
import os
import requests
from datetime import datetime
from supabase import Client
from dotenv import load_dotenv
from database import get_supabase_client

load_dotenv()

# Supabase 클라이언트 초기화
supabase: Client = get_supabase_client()

def fetch_subway_realtime(station: str = "강남역") -> list:
    """
    서울 지하철 실시간 도착 정보 API 호출
    
    Args:
        station: 역 이름 (예: 강남역, 서울역)
    
    Returns:
        list: 실시간 도착 정보 리스트
    """
    api_key = os.getenv("SEOUL_API_KEY")
    # API 키가 URL 인코딩이 필요한 경우도 있으나, 보통은 그대로 사용. 
    # 서울시 API는 끝에 /를 붙여야 하는 경우도 있음. 확인 필요.
    # 포맷: http://swopenAPI.seoul.go.kr/api/subway/(인증키)/json/realtimeStationArrival/0/5/서울역
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
