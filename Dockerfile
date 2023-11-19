# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files into the container
COPY . /app/

# Expose the port that the Flask app will run on
EXPOSE 3338

# Command to run the Flask application
CMD ["python", "app.py"]

