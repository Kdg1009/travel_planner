from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import get_pois, route_optim, ors_proxy, download_plan, cache_routes, user_auth

# to deploy this server:
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
app.include_router(ors_proxy.router, prefix=backend_route_prefix)
app.include_router(download_plan.router, prefix=backend_route_prefix)
app.include_router(cache_routes.router, prefix=backend_route_prefix)
app.include_router(user_auth.router, prefix=backend_route_prefix)