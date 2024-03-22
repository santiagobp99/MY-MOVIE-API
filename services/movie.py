from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        # consultar a movie model
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie_by_id(self, id):
        # consultar a movie model
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        movie_dict = movie.model_dump()
        # MovieModel(title=movie.title, .....)
        new_movie = MovieModel(**movie_dict) # Extraer atributos del diccionario
        self.db.add(new_movie)
        self.db.commit()
        return new_movie
    
    def update_movie(self, id:int, data: Movie) -> None:
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        result.title = data.title
        result.overview = data.overview
        result.year = data.year
        result.rating = data.rating
        result.category = data.category
        self.db.commit()
        return
    
    def delete_movie(self, id:int)-> dict:
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return