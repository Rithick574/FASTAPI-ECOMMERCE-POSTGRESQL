from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from database import engine, Base, get_db

load_dotenv()

app = FastAPI()

client_url = os.getenv("CLIENT_URL")

if client_url is None:
    raise ValueError("CLIENT_URL environment variable is not set in .env file")

origins = [
    client_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", response_model=dict)
def read_root() -> dict:
    return {
        "message": "server is running"
    }

