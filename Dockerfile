# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .
# COPY instance/ instance/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Flask default)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
