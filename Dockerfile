# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory 
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

COPY .env /code/.env

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
