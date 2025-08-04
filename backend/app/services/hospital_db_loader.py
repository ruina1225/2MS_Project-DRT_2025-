import csv
from app.utils.safe_converter import safe_int, safe_float
import pandas as pd
from app.database import get_db_conn

# 원본 파일 경로
input_path = "backend/app/uploads/hopital_data/l_c0903a3bc93d414e8f7b84cd33264ee0.csv"
output_path = "backend/app/uploads/hopital_data/hospitals_geocoded_final.csv"

# CSV 읽기
df = pd.read_csv(input_path, encoding="utf-8-sig")

# 컬럼명 변경 (x → longitude, y → latitude) / 지오코딩에서 x,y로만 저장 가능
df.rename(columns={"type":"hospital_type", "x": "longitude", "y": "latitude"}, inplace=True)

# 새 파일로 저장
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print("✅ 저장 완료: hospitals_geocoded_final.csv")

# Oracle 연결 정보
conn = get_db_conn()
cursor = conn.cursor()

# 지오코딩된 파일 경로
output_path = "backend/app/uploads/hopital_data/ospitals_geocoded_final.csv"  # ← 실제 경로로 바꿔주세요

with open(output_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get("name", "").strip()
        addr = row.get("address", "").strip()
        type_ = row.get("hospital_type", "").strip()
        phone = row.get("phone", "").strip()
        room = safe_int(row.get("room_count", 0))
        bed = safe_int(row.get("bed_count", 0))
        lat = safe_float(row.get("latitude"))
        lon = safe_float(row.get("longitude"))

        if lat is not None and lon is not None:
            print(f"📍 저장: {name}, {addr} → 위도: {lat}, 경도: {lon}")
            cursor.execute("""
                INSERT INTO HOSPITALS_DRT
                (name, address, hospital_type, phone, room_count, bed_count, latitude, longitude)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """, (name, addr, type_, phone, room, bed, lat, lon))
        else:
            print(f"⚠️ 위경도 없음 → 생략: {name}")

    conn.commit()

print("✅ DB 저장 완료")