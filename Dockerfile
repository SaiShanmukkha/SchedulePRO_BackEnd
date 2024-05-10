# Use the official Ubuntu as a parent image
FROM ubuntu:latest

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Create and set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN python -m pip install -r requirements.txt

    # Install Gunicorn
RUN python3 -m pip install gunicorn

# Expose the port Gunicorn will listen on
EXPOSE 8000

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SchedulePRO_Backend.wsgi:application"]
