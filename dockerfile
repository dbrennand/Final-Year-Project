FROM python:3.9-slim

# Set working directory
WORKDIR /usr/src/app

# Copy requirements.txt to /usr/src/app inside the container
COPY requirements.txt ./
# Install the app requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app's source code to /usr/src/app inside the container
COPY . .
