# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /data

# Copy everything into the container
COPY . .

# Set the PYTHONPATH to include the 'src' directory (adjust if needed)
ENV PYTHONPATH=/data/src:$PYTHONPATH

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose your app's port
EXPOSE 8000

# Run the FastAPI app using your GMApp class
CMD ["python", "src/run.py"]
