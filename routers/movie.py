from fastapi import APIRouter

from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse

from typing import List

# Autenticacion
from middlewares.jwt_bearer import JWTBearer

# Base de Datos
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Servicios
from services.movie import MovieService

# Esquemas
from schemas.movie import Movie, CategoryEnum

movie_router = APIRouter()
    

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
  

# La clase que se ejecuta al momento de realizar la peticion es JWTBearer, se ejecuta la funcion call
# @movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
# def get_movies() -> List[Movie]:
#     # return movies
#     return JSONResponse(status_code=200, content=movies)

# DB + La clase que se ejecuta al momento de realizar la peticion es JWTBearer, se ejecuta la funcion call
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).all()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# @movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
# def get_movie_by_id(id:int = Path(ge=1, le=2000)) -> Movie:
#     for item in movies:
#         if item["id"] == id:
#             # return item
#             return JSONResponse(content=item)
#     # return []
#     return JSONResponse(content=[], status_code=404)

# DB
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie_by_id(id:int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(content={'message': "No encontrado"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# @movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
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
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: CategoryEnum) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

# Post No Schema

# @movie_router.post('/movies', tags=['movies'])
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
# @movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
# def create_movie(movie: Movie) -> dict:
#     # Convert the Model to a dictionary representation
#     movies.append(movie.model_dump())
#     # return movies
#     return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)

# Post Schema with db connection
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    # movie_dict = movie.model_dump()
    # # MovieModel(title=movie.title, .....)
    # new_movie = MovieModel(**movie_dict) # Extraer atributos del diccionario
    # db.add(new_movie)
    # db.commit()
    return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)


# Put No Schema
# @movie_router.put('/movies/{id}', tags=['movies'])
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
# @movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
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
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
    # result.title = movie.title
    # result.overview = movie.overview
    # result.year = movie.year
    # result.rating = movie.rating
    # result.category = movie.category
    # db.commit()
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200)
        
    

# # Eliminacion de peliculas
# @movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
# def delete_movie(id:int)-> dict:
#     for item in movies:
#         if item['id'] == id:
#             movies.remove(item)
#             return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=200)
#     else:
#         return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
#         # return "The movie selected, doesnt exist"

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id:int)-> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(content={"message": "The movie selected, doesnt exist"}, status_code=400)
    result = MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=200)