# Use an official Python 3.10 runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip
# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt
