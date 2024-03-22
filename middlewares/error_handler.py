from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.responses import Response

# Creacion de un Middleware para manejo de errores
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        
    # Metodo que se ejecuta para detectar errores en la app
    # call next, mira a la siguinte llamada
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})
        