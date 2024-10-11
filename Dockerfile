# Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the application code
ADD . .

EXPOSE 3000

# Command to run the application
CMD ["python", "app.py"]