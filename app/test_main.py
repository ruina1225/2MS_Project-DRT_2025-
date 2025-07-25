# uvicorn test_main:app --host=0.0.0.0 --port=3434 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user_router, hospital_router, visit_router, locations

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(hospital_router.router, prefix="/hospitals", tags=["Hospitals"])
app.include_router(visit_router, prefix="/visits", tags=["Visits"])
# app.include_router(locations.router, prefix="/locations", tags=["Locations"])
