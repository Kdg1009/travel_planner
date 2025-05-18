from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import get_pois, route_optim

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_pois.router)
app.include_router(route_optim.router)