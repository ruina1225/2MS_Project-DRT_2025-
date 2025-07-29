# app/services/hospital_csv_converter.py
import csv

def save_raw_hospitals_to_csv(hospitals, filepath: str):
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
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

def convert_csv_column_names(input_file: str, output_file: str):
    column_map = {
        "의료기관명": "name",
        "소재지": "address",
        "병원종별": "type",
        "연락처": "phone",
        "병실수": "room_count",
        "병상수": "bed_count",
        "진료과목": "dept_name"
    }

    with open(input_file, newline="", encoding="utf-8-sig") as infile, \
         open(output_file, "w", newline="", encoding="utf-8-sig") as outfile:

        reader = csv.DictReader(infile)
        new_fieldnames = [column_map.get(field, field) for field in reader.fieldnames]
        writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
        writer.writeheader()

        for row in reader:
            new_row = {column_map.get(k, k): v for k, v in row.items()}
            writer.writerow(new_row)
