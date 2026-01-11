# We only need Python now (No Node.js needed!)
FROM python:3.9

WORKDIR /app

# 1. Install Backend Dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy Backend Code
COPY backend/ ./backend
COPY data/ ./data

# 3. Copy the PRE-BUILT Frontend (This is what you built locally)
# We copy it directly from your computer's folder to the container
COPY frontend/dist ./frontend/dist

# 4. Start the Server
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]