# /data şeklinde örnek bir servis yaz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.mlRouter import mlRouter
from .routes.userRoute import userRouter

app = FastAPI()

# cors eklemesi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# userRouter include edilmesi
app.include_router(userRouter, prefix="/user")
app.include_router(mlRouter, prefix="/ml")

