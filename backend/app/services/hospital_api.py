import requests
import csv
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CSV_PATH = os.path.join(BASE_DIR, "app", "uploads", "hospital_data", "myfile.csv")

# API 요청
url = "https://api.odcloud.kr/api/3045143/v1/uddi:a121e723-7ae7-44df-ba6f-86eb09a633e7"
params = {
    "page": 1,
    "perPage": 1000,
    "returnType": "JSON",
    "serviceKey": "xZq/MBrLVT7SuSCy9Xidjni6dYR2XKaI/FPpv+IA8llCj4GN8NIuwL03CuMTvGNK1nakZ7DwO/LFJS+22qGJew=="
}

response = requests.get(url, params=params)
result = response.json()
hospitals = [item for item in result.get("data", []) if item.get("병원종별", "").strip() == "종합병원"]

# CSV로 저장 (지오코딩은 나중에)
with open("backend/app/uploads/hopital_data/hospitals_raw.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["의료기관명", "소재지", "병원종별", "연락처", "병실수", "병상수", "진료과목"])
    for item in hospitals:
        writer.writerow([
            item.get("의료기관명", "").strip(),
            item.get("소재지", "").strip(),
            item.get("병원종별", "").strip(),
            item.get("연락처", "").strip(),
            str(item.get("병실수", "")).strip(),
            str(item.get("병상수", "")).strip(),
            item.get("진료과목", "").strip()
        ])
        
print("✅ 병원 기본정보 파일 저장 완료: hospitals_raw.csv")

# ======== STEP 2: 컬럼명 영어로 변환 ======== # 지오코딩 변환시 컬럼명 영문으로 변경 필요해서 
column_map = {
    "의료기관명": "name",
    "소재지": "address",
    "병원종별": "type",
    "연락처": "phone",
    "병실수": "room_count",
    "병상수": "bed_count",
    "진료과목": "dept_name"
}

input_file = "backend/app/uploads/hopital_data/hospitals_raw.csv"
output_file = "backend/app/uploads/hopital_data/hospitals_english.csv"

with open(input_file, newline="", encoding="utf-8-sig") as infile, \
     open(output_file, "w", newline="", encoding="utf-8-sig") as outfile:

    reader = csv.DictReader(infile)
    new_fieldnames = [column_map.get(field, field) for field in reader.fieldnames]

    writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
    writer.writeheader()

    for row in reader:
        new_row = {column_map.get(k, k): v for k, v in row.items()}
        writer.writerow(new_row)

print("✅ hospitals_english.csv 저장 완료 (영문 컬럼 변환)")