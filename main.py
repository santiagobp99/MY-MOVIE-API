# uvicorn main:app --port 5000 --reload --host

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Base de Datos
from config.database import engine, Base

# Manejo de Errores
from middlewares.error_handler import ErrorHandler

# Routers
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

# El middleware se ejecuta cuando ocurra un error en la aplicacion
app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(movie_router)

# El motor a usar es el que acabo de importar engine
Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def message():
    # return "Hello World!"
    # return {"Hello":"World"}
    return HTMLResponse('<h1> Hello World</h1>')
