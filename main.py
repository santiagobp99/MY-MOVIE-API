# uvicorn main:app --port 5000 --reload --host

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Coroutine, Optional, List

# Autenticacion
from fastapi.security import HTTPBearer
from jwt_manager import create_token, validate_token

# Base de Datos
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

# El motor a usar es el que acabo de importar engine
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # va a devolver el token, datos de las credenciales
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

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
            

movies = [
     {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": CategoryEnum.ACCION
	},
     {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": CategoryEnum.ACCION
	}
]

# {
#   "id": 3,
#   "title": "Iron Man",
#   "overview": "string",
#   "year": 2019,
#   "rating": 10,
#   "category": "Acción"
# }





@app.get('/', tags=['home'])
def message():
    # return "Hello World!"
    # return {"Hello":"World"}
    return HTMLResponse('<h1> Hello World</h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)


# La clase que se ejecuta al momento de realizar la peticion es JWTBearer, se ejecuta la funcion call
# @app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
# def get_movies() -> List[Movie]:
#     # return movies
#     return JSONResponse(status_code=200, content=movies)

# DB + La clase que se ejecuta al momento de realizar la peticion es JWTBearer, se ejecuta la funcion call
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# @app.get('/movies/{id}', tags=['movies'], response_model=Movie)
# def get_movie_by_id(id:int = Path(ge=1, le=2000)) -> Movie:
#     for item in movies:
#         if item["id"] == id:
#             # return item
#             return JSONResponse(content=item)
#     # return []
#     return JSONResponse(content=[], status_code=404)

# DB
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie_by_id(id:int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={'message': "No encontrado"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# @app.get('/movies/', tags=['movies'], response_model=List[Movie])
# def get_movies_by_category(category: CategoryEnum) -> List[Movie]:
#     # selected = []
#     data = [item for item in movies if item["category"] == category]
#         # for item in movies:
#         #     if item["category"] == category:
#         #         data.append(item)
#     # return data
#     print(data)
#     return JSONResponse(content=data)

# DB
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: CategoryEnum) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

# Post No Schema

# @app.post('/movies', tags=['movies'])
# def create_movie(id:int = Body(), title:str = Body(), overview:str = Body(), year:int = Body(), rating:float = Body(), category:str = Body()):
#     movies.append({
#         "id": id,
# 		"title": title,
# 		"overview": overview,
# 		"year": year,
# 		"rating": rating,
# 		"category": category
#     })
#     return movies


# # Post Schema
# @app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
# def create_movie(movie: Movie) -> dict:
#     # Convert the Model to a dictionary representation
#     movies.append(movie.model_dump())
#     # return movies
#     return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)

# Post Schema with db connection
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    movie_dict = movie.model_dump()
    # MovieModel(title=movie.title, .....)
    new_movie = MovieModel(**movie_dict) # Extraer atributos del diccionario
    db.add(new_movie)
    db.commit()
    # movies.append(movie_dict)
    return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)


# Put No Schema
# @app.put('/movies/{id}', tags=['movies'])
# def update_movie(id:int, title:str = Body(), overview:str = Body(), year:int = Body(), rating:float = Body(), category:str = Body()):
#     for item in movies:
#         if item['id'] == id:
#             item["title"] = title
#             item["overview"] = overview
#             item["year"] = year
#             item["rating"] = rating
#             item["category"] = category
#             return movies
#     else:
#         return "The movie selected, doesnt exist"



# # Modificacion de peliculas
# @app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
# def update_movie(id:int, movie: Movie) -> dict:
#     for item in movies:
#         if item['id'] == id:
#             item["title"] = movie.title
#             item["overview"] = movie.overview
#             item["year"] = movie.year
#             item["rating"] = movie.rating
#             item["category"] = movie.category
#             return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200)
#     else:
#         return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)

# DB + Modificacion de peliculas
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200)
        
    

# # Eliminacion de peliculas
# @app.delete('/movies/{id}', tags=['movies'], response_model=dict)
# def delete_movie(id:int)-> dict:
#     for item in movies:
#         if item['id'] == id:
#             movies.remove(item)
#             return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=200)
#     else:
#         return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
#         # return "The movie selected, doesnt exist"

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id:int)-> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=200)