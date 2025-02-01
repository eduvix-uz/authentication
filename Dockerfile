# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy the rest of the application code
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=authenticator_service.settings

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["bash", "-c", "python manage.py makemigrations users && python manage.py migrate users && python manage.py collectstatic --noinput && gunicorn authenticator_service.wsgi:application --bind 0.0.0.0:8000"]
