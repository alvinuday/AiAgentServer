FROM python:3.11
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optionally: Copy the .env file (if needed during the build process)
# You can skip this if you want to pass .env during runtime using --env-file
# COPY .env /app/.env

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "main.py"]