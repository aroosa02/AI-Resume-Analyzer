FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/ /app/backend/

# Expose the port that the application will run on
EXPOSE 8000

# Railway provides a PORT environment variable dynamically.
# We bind Uvicorn to 0.0.0.0 and the PORT provided by Railway (or fallback to 8000).
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
