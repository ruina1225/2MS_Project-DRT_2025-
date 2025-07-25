from fastapi import APIRouter
from app.database import get_db_conn

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_visits(user_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            u.user_id, u.name, u.birth_date, u.identifier_code,
            h.hospital_id, h.name, h.address, h.latitude, h.longitude,
            v.visit_time, v.origin_lat, v.origin_lng, v.dest_lat, v.dest_lng
        FROM VISITS_DRT v
        JOIN USERS_DRT u ON v.user_id = u.user_id
        JOIN HOSPITALS_DRT h ON v.hospital_id = h.hospital_id
        WHERE u.user_id = :user_id
        ORDER BY v.visit_time DESC
    """, {"user_id": user_id})
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"user_visits": [
        {
            "user_id": row[0],
            "user_name": row[1],
            "birth_date": row[2].strftime("%Y-%m-%d"),
            "identifier_code": row[3],
            "hospital_id": row[4],
            "hospital_name": row[5],
            "address": row[6],
            "latitude": float(row[7]) if row[7] else None,
            "longitude": float(row[8]) if row[8] else None,
            "visit_time": row[9].strftime("%Y-%m-%d %H:%M:%S"),
            "origin_lat": float(row[10]) if row[10] else None,
            "origin_lng": float(row[11]) if row[11] else None,
            "dest_lat": float(row[12]) if row[12] else None,
            "dest_lng": float(row[13]) if row[13] else None,
        }
        for row in rows
    ]}
