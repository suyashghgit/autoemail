FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8000

# Run the application with explicit reload and access-log settings
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 