# Base image with Python
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt (make sure you have it with Streamlit and any other dependencies listed)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Taipy
EXPOSE 8000

# Command to run the Streamlit app
CMD ["bash"]