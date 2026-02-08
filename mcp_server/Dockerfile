# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the mcp_server directory to the working directory
COPY mcp_server/mcp_server.py .

# Make port 8000 available to the world outside this container
EXPOSE 8002

# Run mcp_server.py when the container launches
CMD ["uvicorn", "mcp_server:mcp", "--host", "0.0.0.0", "--port", "8002"]
