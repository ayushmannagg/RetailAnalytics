from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import sales
from seed import seed_data
import os 
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Retail Analytics API")

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

BASE_DIR = Path(__file__).resolve().parent.parent

DIST_DIR = BASE_DIR / "frontend" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(sales.router)

assets_path = DIST_DIR / "assets"
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

if os.path.exists("../frontend/dist"):
    app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # If the path is an API call, ignore it (FastAPI handles it above)
    if full_path.startswith("sales"):
        return {"error": "API route not found"}
    
    # Check if index.html exists
    index_path = DIST_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
        
    return {"message": "Frontend not built. Check 'frontend/dist' folder."}

@app.get("/seed-db")
def trigger_seeding():
    try:
        seed_data()
        return {"status": "success", "message": "Database has been seeded with cloud data!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/")
def root():
    return {"message": "System is Online"}