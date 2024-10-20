import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.database import users, admin_password
from app.users.auth import get_password_hash
from app.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)


# class AdminPass(BaseModel):
#     unique_id: int
#     admin_password: bytes


@app.on_event("startup")
async def startup_db():
    await users.create_index("email", unique=True)

    # await admin_password.create_index("unique_id", unique=True)
    # password = await get_password_hash("qazwsxedc123+")
    # admin_hash = AdminPass(unique_id=1, admin_password=password)
    # await admin_password.insert_one(admin_hash.model_dump())

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
    ],
)
