from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import sales
from seed import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Retail Analytics API")

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/seed-db")
def trigger_seeding():
    try:
        seed_data()
        return {"status": "success", "message": "Database has been seeded with cloud data!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(sales.router)

@app.get("/")
def root():
    return {"message": "System is Online"}