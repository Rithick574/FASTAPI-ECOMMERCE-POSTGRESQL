from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.database import engine, Base, get_db, test_connection
from app.routers import auth, product, cart

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

BASE_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=f"{BASE_PREFIX}/auth", tags=["auth"])
app.include_router(product.router, prefix=f"{BASE_PREFIX}/products", tags=["products"])
app.include_router(cart.router, prefix=f"{BASE_PREFIX}/cart", tags=["Cart"])

@app.get("/",
    response_model=dict,
    tags=["Root"],
    summary="Root endpoint",
    description="Returns a welcome message"
)
def read_root() -> dict:
    return {"Hello": "Welcome to the E-commerce API"}

@app.get("/test-db")
async def test_db_connection():
    if await test_connection():
        return {"status": "success", "message": "Database connection successful"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.on_event("startup")
async def startup_event():
    """
    Verify database connection on startup
    """
    if not await test_connection():  
        raise Exception("Could not connect to database")
    print("Database connection verified during startup!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)