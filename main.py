from models.classes import User, Task
from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from db import create_db_connection

# Создаем основной объект FastAPI
app = FastAPI()

users = [
    User(id=1, name="User 1", email="olya@email.ru"),
    User(id=2, name="User 2", email="katya@email.ru"),
]

users_task = [
    Task(id=1, id_user=1, title="работа", content="совещание в 12:00"),
    Task(id=2, id_user=2, title="праздники", content="день рождения дочери")
]

# Создаем объект APIRouter для работы с пользователями
users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Создаем объект APIRouter для работы с задачами
users_task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

# Создаем методы для работы с пользователями

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class TaskCreate(BaseModel):
    title: str
    content: str


class TaskUpdate(BaseModel):
    title: str
    content: str


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str

@users_router.get("/")
def get_users():
    db = create_db_connection()
    user = db.query(User).all()
    return users

@users_router.get("/{user_id}")
def get_user(user_id: int):
    db = create_db_connection()
    user = db.query(User).get(user_id)
    return user

@users_router.post("/")
def create_user(user: UserCreate):
    db = create_db_connection()
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@users_router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    db = create_db_connection()
    db.query(User).filter(User.id == user_id).update(user.dict())
    db.commit()
    return {"message": "User updated successfully"}

@users_router.delete("/{user_id}")
def delete_user(user_id: int):
    db = create_db_connection()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted successfully"}

# Создаем методы для работы с задачами пользователя

@users_task_router.get("/")
def get_tasks():
    db = create_db_connection()
    tasks = db.query(Task).all()
    return tasks


@users_task_router.get("/{task_id}")
def get_task(task_id: int):
    db = create_db_connection()
    task = db.query(Task).get(task_id)
    return task


@users_task_router.post("/")
def create_task(task: TaskCreate):
    db = create_db_connection()
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@users_task_router.delete("/{task_id}")
def delete_task(task_id: int):
    db = create_db_connection()
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
    return {"message": "Task deleted successfully"}

# Подключаем маршруты для работы с пользователями к приложению
app.include_router(users_router)
app.include_router(users_task_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)