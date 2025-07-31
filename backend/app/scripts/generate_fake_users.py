import os # 파일 및 디렉토리 작업을 위한 표준 라이브러리
import uuid # 고유한 UUID(고유 식별자)를 생성하기 위한 라이브러리
from faker import Faker # Faker는 가짜 이름, 생일 등 더미 데이터를 생성하기 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리
import shutil # 파일 복사 등을 처리하기 위한 라이브러리

fake = Faker('ko_KR')  # 한국어 설정으로 Faker 인스턴스를 생성 (한국식 이름 등 생성 가능)

# 현재 파일 기준 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 프로젝트 루트(app 폴더) 기준 uploads 경로로 수정
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads") # 원본 이미지가 있는 기본 폴더
UUID_IMG_DIR = os.path.join(UPLOAD_DIR, "uuid_img") # UUID로 바꾼 이미지 저장 폴더 (uploads/uuid_img)

# uuid_img 폴더 없으면 생성
os.makedirs(UUID_IMG_DIR, exist_ok=True)

# API 주소
API_URL = "http://localhost:3434/users/add-photo" # 사진과 사용자 정보를 보낼 API 엔드포인트

# 업로드할 사진 파일들만 필터링
photo_files = sorted([
    f for f in os.listdir(UPLOAD_DIR)
    if f.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.isfile(os.path.join(UPLOAD_DIR, f))
])

# 최소 30장 확인
if len(photo_files) < 30:
    print(f"❌ 사진이 30장보다 적습니다. 현재 사진 개수: {len(photo_files)}")
    exit()

# 30개 사용자 데이터 생성 및 사진 전송
for i in range(30):
    name = fake.name() # 가짜 사용자 이름 생성
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=80).strftime('%Y-%m-%d') # 생일 생성 후 문자열로 포맷

    original_photo_path = os.path.join(UPLOAD_DIR, photo_files[i]) # 원본 이미지 경로 생성

    # UUID 파일명 생성
    ext = os.path.splitext(photo_files[i])[1] # 파일 확장자 추출 (예: ".jpg")
    uuid_filename = f"{uuid.uuid4()}{ext}" # UUID를 파일 이름으로 사용하고 확장자는 유지
    uuid_photo_path = os.path.join(UUID_IMG_DIR, uuid_filename) # 변경된 이름으로 저장될 경로

    # 원본 파일을 uuid_img에 복사
    shutil.copy2(original_photo_path, uuid_photo_path)

    # API 업로드 요청
    with open(uuid_photo_path, "rb") as photo_file: # 변경된 이미지 파일을 이진 모드로 열기
        files = {"photo": (uuid_filename, photo_file, "image/jpeg")} # 파일 업로드를 위한 multipart 구성
        data = {
            "name": name,
            "birth_date": birth_date
        }

        try:
            res = requests.post(API_URL, data=data, files=files) # FastAPI 서버로 POST 요청 (multipart/form-data)
            print(f"[{i+1}] ✅ 등록 완료:", res.json()) # 응답 JSON 출력
        except requests.exceptions.RequestException as e: # 네트워크 오류 등 예외 발생 시
            print(f"[{i+1}] ❌ 오류 발생:", e)
            break  # 에러 발생 시 반복문 종료



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
