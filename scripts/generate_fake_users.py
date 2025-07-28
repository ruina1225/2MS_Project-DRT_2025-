
from faker import Faker
import requests
import os

fake = Faker('ko_KR') # 한국어 기반 가짜 데이터 생성 라이브러리(FAKER)

UPLOAD_DIR = "uploads"  # 사진 폴더
API_URL = "http://localhost:3434/users/add-photo"

photo_files = sorted([f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

if len(photo_files) < 30:
    print(f"❌ 사진이 30장보다 적습니다. 현재 사진 개수: {len(photo_files)}")
    exit()

for i in range(30):
    name = fake.name()
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d')
    photo_path = os.path.join(UPLOAD_DIR, photo_files[i])

    with open(photo_path, "rb") as photo_file:
        files = {"photo": (photo_files[i], photo_file, "image/jpeg")}
        data = {
            "name": name,
            "birth_date": birth_date
        }

        try:
            res = requests.post(API_URL, data=data, files=files)
            print(f"[{i+1}] ✅ 등록 완료:", res.json())
        except requests.exceptions.RequestException as e:
            print(f"[{i+1}] ❌ 오류 발생:", e)
            break



# from faker import Faker
# import requests


# fake = Faker('ko_KR')

# for _ in range(30):
#     name = fake.name()
#     birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d')
#     identifier = fake.unique.bothify(text='??######')

#     payload = {
#         "name": name,
#         "birth_date": birth_date,
#         "identifier_code": identifier
#     }

#     try:
#         res = requests.post("http://localhost:3434/users/add", json=payload)
#         print(res.json())
#     except requests.exceptions.ConnectionError:
#         print("❌ 서버가 실행 중이 아닙니다. FastAPI를 먼저 실행하세요.")
#         break
