from fastapi import APIRouter
from app.database import get_db_conn

router = APIRouter()

@router.get("/")
async def get_hospitals():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hospital_id FROM hospitals_drt")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"hospitals": [row[0] for row in rows]}
