# Use python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# expose port 8000
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "3", "--threads", "3", "app:app"]