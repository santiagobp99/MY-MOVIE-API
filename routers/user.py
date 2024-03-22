from fastapi import APIRouter

from pydantic import BaseModel, ConfigDict
from fastapi.responses import JSONResponse

# Autenticacion
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email:str
    password:str
    
    model_config = ConfigDict(json_schema_extra={
        'examples': [
                {
                    "email": "admin@gmail.com",
                    "password": "admin"
                }
            ]
    })
    

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)