from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import sales
from seed import seed_data
import os 

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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if os.path.exists("../frontend/dist"):
    app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # If the path is an API call, ignore it (FastAPI handles it above)
    if full_path.startswith("sales"):
        return {"error": "API route not found"}
    
    # Otherwise, return the React App
    if os.path.exists("../frontend/dist/index.html"):
        return FileResponse("../frontend/dist/index.html")
    return {"message": "Frontend not built. Run 'npm run build' first."}

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