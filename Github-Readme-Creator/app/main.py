from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from fastapi.responses import ORJSONResponse

app = FastAPI(title="GitHub README Generator", default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)