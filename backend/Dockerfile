# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY src/ ./src/

# Create and switch to a non-root user
RUN useradd app
USER app

# Expose the port
EXPOSE 8000

# Run the Django application
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]