# /data şeklinde örnek bir servis yaz
from fastapi import FastAPI

from .routes.mlRouter import mlRouter
from .routes.userRoute import userRouter

app = FastAPI()

# userRouter include edilmesi
app.include_router(userRouter, prefix="/user")
app.include_router(mlRouter, prefix="/ml")

