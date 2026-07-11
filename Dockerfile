
# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (app.py, templates, static)
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

