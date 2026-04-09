from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Laboratorio de Seguridad ")

class User(BaseModel):
    id: int
    username: str
    password: str
    is_active: bool = True

db_users = [
    {"id": 1, "username": "admin", "password": "password123", "is_active": True},
    {"id": 2, "username": "estudiante", "password": "uide", "is_active": True}
]

@app.get("/users", response_model=List[User])
def get_users():
    return db_users

@app.post("/users", status_code=201)
def create_user(user: User):
    if any(u['username'] == user.username for u in db_users):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    db_users.append(user.dict())
    return {"message": "Usuario creado con éxito"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in db_users if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global db_users
    db_users = [u for u in db_users if u['id'] != user_id]
    return {"message": "Usuario eliminado"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    user = next((u for u in db_users if u['username'] == request.username), None)
    
    if user and user['password'] == request.password:
        return {"status": "success", "message": "Login exitoso"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Login fallido: credenciales incorrectas"
    )