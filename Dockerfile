FROM python:3.7

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

RUN pip install --upgrade pip

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY openapi_server ./openapi_server

# Expose port
EXPOSE 8080

# Set the entrypoint command to run the FastAPI server
CMD ["uvicorn", "openapi_server.main:app", "--host", "0.0.0.0", "--port", "8080"]
