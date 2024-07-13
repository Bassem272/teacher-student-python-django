# # Use an official Python runtime as a parent image
# FROM python:3.9

# # Set the working directory to the root of your Django project
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libssl-dev \
#     libffi-dev \
#     python3-dev \
#     zlib1g-dev \
#     libbz2-dev \
#     libreadline-dev \
#     libsqlite3-dev \
#     wget \
#     curl \
#     llvm \
#     libncurses5-dev \
#     libncursesw5-dev \
#     xz-utils \
#     tk-dev \
#     libxml2-dev \
#     libxmlsec1-dev \
#     libffi-dev \
#     liblzma-dev \
#     libgdbm-dev \
#     libc6-dev \
#     libyaml-dev \
#     libpq-dev \
#     libiodbc2-dev \
#     libcurl4-openssl-dev \
#     gcc

# # Copy the requirements file
# COPY requirements.txt ./

# # Install dependencies
# RUN pip install -r requirements.txt

# # Install cron
# RUN apt-get update && apt-get install -y cron

# # Install necessary additional packages for Django Channels and Redis
# RUN pip install daphne channels redis

# # Install Redis server
# RUN apt-get install -y redis-server

# # Copy the rest of your application
# COPY . .

# # Copy Google Cloud credentials file
# COPY creds.json /app/creds.json

# # Set environment variables
# ENV EMAIL_USE_TLS=True
# ENV EMAIL_PORT=587
# ENV GOOGLE_CLOUD_PROJECT=dragna272
# # Add other environment variables as needed
# ENV GOOGLE_APPLICATION_CREDENTIALS /path/to/creds.json

# # Cron job command (replace with your Django management command)
# RUN echo "* * * * * cd /app && python manage.py runserver 0.0.0.0:8000 >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job

# # Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/my-cron-job

# # Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# # Expose port 8000 (the port on which Django server runs) and Redis port
# EXPOSE 8000
# EXPOSE 6379

# # Run the Redis server in the background and then start Daphne with Django
# CMD ["bash", "-c", "redis-server --daemonize yes && daphne -b 0.0.0.0 -p 8000 cplatform.asgi:application"]

# Use an official Python runtime as a parent image
# FROM python:3.9

# # Set the working directory to the root of your Django project
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libssl-dev \
#     libffi-dev \
#     python3-dev \
#     zlib1g-dev \
#     libbz2-dev \
#     libreadline-dev \
#     libsqlite3-dev \
#     wget \
#     curl \
#     llvm \
#     libncurses5-dev \
#     libncursesw5-dev \
#     xz-utils \
#     tk-dev \
#     libxml2-dev \
#     libxmlsec1-dev \
#     libffi-dev \
#     liblzma-dev \
#     libgdbm-dev \
#     libc6-dev \
#     libyaml-dev \
#     libpq-dev \
#     libiodbc2-dev \
#     libcurl4-openssl-dev \
#     gcc \
#     cron \
#     redis-server

# # Copy the requirements file
# COPY requirements.txt ./

# # Install necessary additional packages for Django Channels and Redis
# RUN pip install daphne channels redis

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application code
# COPY . .

# # Copy Google Cloud credentials file
# COPY creds.json /app/creds.json

# # Set environment variables
# ENV EMAIL_USE_TLS=True
# ENV EMAIL_PORT=587
# ENV GOOGLE_CLOUD_PROJECT=dragna272
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/creds.json
# # Add other environment variables as needed

# # Create a cron job for Django management commands
# RUN echo "* * * * * cd /app && python manage.py runserver 0.0.0.0:8000 >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job
# RUN chmod 0644 /etc/cron.d/my-cron-job
# RUN touch /var/log/cron.log

# # Expose port 8000 (Django server) and 6379 (Redis)
# EXPOSE 8000
# EXPOSE 6379

# # Start Redis server and Daphne with Django
# CMD ["bash", "-c", "redis-server --daemonize yes && daphne -b 0.0.0.0 -p 8000 cplatform.asgi:application"]

# Use an official Python runtime as a parent image for backend
FROM python:3.9 as backend

# Set the working directory to the root of your Django project
WORKDIR /app/backend

# Install system dependencies for Django and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    libgdbm-dev \
    libc6-dev \
    libyaml-dev \
    libpq-dev \
    libiodbc2-dev \
    libcurl4-openssl-dev \
    gcc \
    cron \
    redis-server

# Copy the backend project files into the container
COPY teacher-student-python-django/ /app/backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Optionally copy Google Cloud credentials file if needed
COPY teacher-student-python-django/creds.json /app/creds.json

# Set environment variables
ENV EMAIL_USE_TLS=True
ENV EMAIL_PORT=587
ENV GOOGLE_CLOUD_PROJECT=dragna272
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/creds.json

# Create a cron job for Django management commands
RUN echo "* * * * * cd /app/backend && python manage.py runserver 0.0.0.0:8000 >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN touch /var/log/cron.log

# Expose port 8000 (Django server) and 6379 (Redis)
EXPOSE 8000
EXPOSE 6379
