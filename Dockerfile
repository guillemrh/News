# Use a base Python image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code into the container
COPY . .

# Execute the application when the container starts
CMD ["python", "main.py"]