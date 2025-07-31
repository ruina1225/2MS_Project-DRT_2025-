#수정해야해요 ~~~~~ 250731

import csv
import oracledb

# Oracle 연결 정보
dsn = oracledb.makedsn("195.168.9.216", 1521, service_name="xe")
con = oracledb.connect(user="mb", password="mobridge", dsn=dsn)
cursor = con.cursor()

# CSV 파일 경로
csv_path = r"새 폴더\\MS_Project-DRT_2025-\\DB\\hospital\\files\\hospitals_english.csv"

# 부서 데이터 삽입
with open(csv_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        hospital_name = row.get("name", "").strip()
        dept_field = row.get("dept_name", "").strip()

        # 병원 ID 조회
        cursor.execute("""
            SELECT hospital_id FROM HOSPITALS_DRT WHERE name = :1
        """, (hospital_name,))
        result = cursor.fetchone()

        if result:
            hospital_id = result[0]

            # 부서명 분리 (쉼표 또는 공백 기준)
            depts = [dept.strip() for dept in dept_field.replace(",", " ").split() if dept.strip()]

            for dept in depts:
                # 이미 같은 병원+부서 조합이 있는지 확인 (중복 방지 선택적)
                cursor.execute("""
                    SELECT COUNT(*) FROM HOSPITAL_DEPTS_DRT
                    WHERE hospital_id = :1 AND dept_name = :2
                """, (hospital_id, dept))
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.execute("""
                        INSERT INTO HOSPITAL_DEPTS_DRT (hospital_id, dept_name)
                        VALUES (:1, :2)
                    """, (hospital_id, dept))
                    print(f"➕ 부서 추가: {hospital_name} → {dept}")
                else:
                    print(f"⚠️ 이미 존재: {hospital_name} → {dept}")
        else:
            print(f"❌ 병원 없음 → 생략: {hospital_name}")

    con.commit()

cursor.close()
con.close()
print("✅ 모든 부서 입력 완료")
