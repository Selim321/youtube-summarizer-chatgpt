# Use a base image with Python preinstalled
FROM python:3.11.5-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install app dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080","--server.address=0.0.0.0"]
