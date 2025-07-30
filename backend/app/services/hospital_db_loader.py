# app/services/hospital_db_loader.py
import csv
import oracledb
from app.utils.safe_converter import safe_int, safe_float

def insert_hospitals_from_csv(file_path: str, db_config: dict):
    dsn = oracledb.makedsn(
        db_config["host"],
        db_config["port"],
        service_name=db_config["service_name"]
    )

    con = oracledb.connect(user=db_config["user"], password=db_config["password"], dsn=dsn)
    cursor = con.cursor()

    with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("name", "").strip()
            addr = row.get("address", "").strip()
            type_ = row.get("hospital_type", row.get("type", "")).strip()
            phone = row.get("phone", "").strip()
            room = safe_int(row.get("room_count"))
            bed = safe_int(row.get("bed_count"))
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

        con.commit()
        con.close()

    print("✅ DB 저장 완료")
