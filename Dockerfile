# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (For psycopg2 / pgvector if needed)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install langgraph langchain-core langchain-groq duckduckgo-search psycopg2-binary uvicorn sqlalchemy

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run Uvicorn backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
