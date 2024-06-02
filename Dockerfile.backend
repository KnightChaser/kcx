# Dockerfile for FastAPI backend

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]