import os
import uuid
from faker import Faker
import requests
import shutil

fake = Faker('ko_KR')  # 한국어 faker

# generate_fake_users.py 파일 기준 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 프로젝트 루트 기준 uploads 폴더 (generate_fake_users.py가 루트에 있다면 그냥 uploads)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

UUID_IMG_DIR = os.path.join(UPLOAD_DIR, "uuid_img")
os.makedirs(UUID_IMG_DIR, exist_ok=True)  # uuid_img 폴더 없으면 생성

API_URL = "http://localhost:3434/users/add-photo"

photo_files = sorted([
    f for f in os.listdir(UPLOAD_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.isfile(os.path.join(UPLOAD_DIR, f))
])

if len(photo_files) < 30:
    print(f"❌ 사진이 30장보다 적습니다. 현재 사진 개수: {len(photo_files)}")
    exit()

for i in range(30):
    name = fake.name()
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d')

    original_photo_path = os.path.join(UPLOAD_DIR, photo_files[i])

    # UUID로 파일명 변경 (복사 경로: uploads/uuid_img)
    ext = os.path.splitext(photo_files[i])[1]
    uuid_filename = f"{uuid.uuid4()}{ext}"
    uuid_photo_path = os.path.join(UUID_IMG_DIR, uuid_filename)

    # 원본 사진을 uuid_img 폴더에 복사 및 이름 변경
    shutil.copy2(original_photo_path, uuid_photo_path)

    # 복사한 UUID 파일을 API로 업로드
    with open(uuid_photo_path, "rb") as photo_file:
        files = {"photo": (uuid_filename, photo_file, "image/jpeg")}
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
# import os
# import uuid
# import shutil

# fake = Faker('ko_KR')  # 한국어 faker

# UPLOAD_DIR = "uploads"  # 원본 사진 폴더
# UUID_IMG_DIR = os.path.join(UPLOAD_DIR, "uuid_img")  # UUID 사진 저장 폴더
# os.makedirs(UUID_IMG_DIR, exist_ok=True)  # uuid_img 폴더 없으면 생성

# API_URL = "http://localhost:3434/users/add-photo"

# photo_files = sorted([
#     f for f in os.listdir(UPLOAD_DIR)
#     if f.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.isfile(os.path.join(UPLOAD_DIR, f))
# ])

# if len(photo_files) < 30:
#     print(f"❌ 사진이 30장보다 적습니다. 현재 사진 개수: {len(photo_files)}")
#     exit()

# for i in range(30):
#     name = fake.name()
#     birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d')

#     original_photo_path = os.path.join(UPLOAD_DIR, photo_files[i])

#     # UUID로 파일명 변경 (복사 경로: uploads/uuid_img)
#     ext = os.path.splitext(photo_files[i])[1]
#     uuid_filename = f"{uuid.uuid4()}{ext}"
#     uuid_photo_path = os.path.join(UUID_IMG_DIR, uuid_filename)

#     # 원본 사진을 uuid_img 폴더에 복사 및 이름 변경
#     shutil.copy2(original_photo_path, uuid_photo_path)

#     # 복사한 UUID 파일을 API로 업로드
#     with open(uuid_photo_path, "rb") as photo_file:
#         files = {"photo": (uuid_filename, photo_file, "image/jpeg")}
#         data = {
#             "name": name,
#             "birth_date": birth_date
#         }

#         try:
#             res = requests.post(API_URL, data=data, files=files)
#             print(f"[{i+1}] ✅ 등록 완료:", res.json())
#         except requests.exceptions.RequestException as e:
#             print(f"[{i+1}] ❌ 오류 발생:", e)
#             break



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
