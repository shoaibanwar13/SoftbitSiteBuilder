# Use an official Python runtime as a parent image
FROM python:3-slim-buster
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt 
# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . .
# Expose port 8000 to allow communication to/from server
EXPOSE 8000
# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Websitegenerator.wsgi:application"]
