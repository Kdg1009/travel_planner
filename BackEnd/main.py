from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import get_pois, route_optim, save_pois

# to run this server:
# uvicorn main:app -reload
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
backend_route_prefix = '/api'
app.include_router(get_pois.router, prefix=backend_route_prefix)
app.include_router(route_optim.router, prefix=backend_route_prefix)
app.include_router(save_pois.router, prefix=backend_route_prefix)