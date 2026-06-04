# userRoute 
from fastapi import APIRouter

from src.models.userAddRequest import UserAddRequest
from src.utils.dummy import allUserData

userRouter = APIRouter()
users = allUserData()

# add post method to add user
@userRouter.post("/add")
def add_user(request: UserAddRequest):
    users.append(request)
    return {"message": "User added successfully", "user": request}
    
# all users get method
@userRouter.get("/all")
def get_all_users():
    return {"users": users}


# get user by id
@userRouter.get("/{user_id}")
def get_user_by_id(user_id: int):
    for user in users:
        if user.id == user_id:
            return {"user": user}
    return {"message": "User not found"}


# delete user by id
@userRouter.delete("/{user_id}")
def delete_user_by_id(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "User deleted successfully"}
    return {"message": "User not found"}

# update user by id
@userRouter.put("/{user_id}")
def update_user_by_id(user_id: int, request: UserAddRequest):
    for user in users:
        if user.id == user_id:
            user.name = request.name
            user.surname = request.surname
            user.email = request.email
            user.password = request.password
            return {"message": "User updated successfully", "user": user}
    return {"message": "User not found"}