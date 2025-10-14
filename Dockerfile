FROM python:3.11.13-slim

# Use a lean working directory and copy only what's necessary to build
WORKDIR /app

# Install dependencies first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app

# For Debian/Ubuntu based slim image

# Expose the typical FastAPI port used by uvicorn in compose (8000)
EXPOSE 8000
ENV PYTHONPATH=/app
# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]