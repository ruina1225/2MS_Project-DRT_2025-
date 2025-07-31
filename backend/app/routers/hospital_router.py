from fastapi import APIRouter
from app.database import get_db_conn
from app.services.hospital_db_loader import insert_hospitals_from_csv

import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()  # .env에서 API_KEY 등 불러오기875

@router.get("/")
async def get_hospitals():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hospital_id FROM hospitals_drt")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"hospitals": [row[0] for row in rows]}

# @router.post("/fetch-and-save")
# def fetch_and_save_hospitals():
#     API_KEY = os.getenv("API_KEY")
#     if not API_KEY:
#         return {"error": "API_KEY not found"}

#     # 절대 경로 기준 설정
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # app/routers 의 부모 폴더 app
#     UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "hospital_data")

#     # 업로드 폴더가 없으면 생성
#     os.makedirs(UPLOAD_DIR, exist_ok=True)

#     RAW_PATH = os.path.join(UPLOAD_DIR, "hospitals_raw.csv")
#     ENG_PATH = os.path.join(UPLOAD_DIR, "hospitals_english.csv")
#     GEOCODED_PATH = os.path.join(UPLOAD_DIR, "hospitals_geocoded_final.csv")

#     DB_CONFIG = {
#         "host": os.getenv("ORACLE_HOST", "195.168.9.216"),
#         "port": int(os.getenv("ORACLE_PORT", 1521)),
#         "service_name": os.getenv("ORACLE_SERVICE_NAME", "xe"),
#         "user": os.getenv("ORACLE_USER", "mb"),
#         "password": os.getenv("ORACLE_PASSWORD", "mobridge")
#     }

#     # 1. API에서 데이터 가져오기
#     hospitals = fetch_hospital_data(API_KEY)

#     # 2. CSV 저장
#     save_raw_hospitals_to_csv(hospitals, RAW_PATH)
#     convert_csv_column_names(RAW_PATH, ENG_PATH)

#     # # (3단계: geocoding 후 GEOCODED_PATH 생성 필요, 여기는 생략)
#     # # 실제 geocoding 함수가 있다면 여기서 호출 필요

#     # # 4. Oracle DB에 저장
#     # insert_hospitals_from_csv(GEOCODED_PATH, DB_CONFIG)

#     # return {"message": "병원 정보 저장 완료"}
