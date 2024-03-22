from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional

class CategoryEnum(str, Enum):
    ACCION = 'Acción'
    DRAMA = 'Drama'
    TERROR = 'Terror'
     

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: CategoryEnum
        
    model_config = ConfigDict(json_schema_extra={
        'examples': [
                {
                    # "id": 1, No requerido al usar db
                    "title": "Mi pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year":2022,
                    "rating": 9.8,
                    "category": CategoryEnum.ACCION
                }
            ]
    })