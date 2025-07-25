from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.database import get_db_conn
from app.utils.uuid_generator import generate_uuid
import shutil
import os
from fastapi.responses import FileResponse

router = APIRouter()
#사용자 정보관리==========================
@router.get("/")
async def get_users():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, birth_date, identifier_code FROM users_drt ORDER BY user_id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"users": [
        {
            "user_id": row[0],
            "name": row[1],
            "birth_date": row[2].strftime("%Y-%m-%d"),
            "identifier_code": row[3],
        } for row in rows
    ]}

@router.post("/")
async def create_user(
    name: str = Form(...),
    birth_date: str = Form(...),
    identifier_code: str = Form(...)
):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users_drt (name, birth_date, identifier_code)
        VALUES (:name, TO_DATE(:birth_date, 'YYYY-MM-DD'), :identifier_code)
    """, {"name": name, "birth_date": birth_date, "identifier_code": identifier_code})
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "사용자 추가 완료"}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_drt WHERE user_id = :user_id", {"user_id": user_id})
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "사용자 삭제 완료"}

#============================================================

@router.get("/{user_id}")
def get_user(user_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, birth_date FROM users_drt WHERE user_id = :id", {"id": user_id})
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user_id": user_id, "name": row[0], "birth_date": row[1]}

#==================================================================

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # uploads 디렉토리가 없으면 생성

#uuid 파일 저장 
@router.post("/")
def create_user(
    name: str = Form(...),
    birth_date: str = Form(...),
    photo: UploadFile = File(...)
):
    conn = get_db_conn()
    cursor = conn.cursor()

    # UUID 생성해서 사진 이름으로 사용
    identifier_code = generate_uuid()
    file_ext = os.path.splitext(photo.filename)[-1]
    filename = f"{identifier_code}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 사진 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # DB 저장
    try:
        cursor.execute("""
            INSERT INTO USERS_DRT (name, birth_date, identifier_code)
            VALUES (:name, :birth_date, :identifier_code)
        """, {
            "name": name,
            "birth_date": birth_date,
            "identifier_code": identifier_code
        })
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {
        "message": "User created successfully",
        "identifier_code": identifier_code,
        "photo_filename": filename
    }

# react로 사진 볼수 있게 api작업
@router.get("/photo/{identifier_code}")
def get_user_photo(identifier_code: str):
    """
    identifier_code에 해당하는 사용자 사진 반환
    """
    # 확장자 없이 저장된 identifier_code 기준으로 실제 파일 찾기
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        file_path = os.path.join(UPLOAD_DIR, f"{identifier_code}{ext}")
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type=f"image/{ext.strip('.')}")
    
    raise HTTPException(status_code=404, detail="Photo not found")