from pydantic import BaseModel, ConfigDict

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