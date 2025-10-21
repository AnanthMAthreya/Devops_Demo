FROM python:3.10-slim

WORKDIR /app

# Install pip and build dependencies (if any)
RUN python -m pip install --upgrade pip

# Copy only requirements first to leverage layer cache
COPY requirements.txt .

# Install dependencies (also install gunicorn to run the app)
RUN python -m pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application source
COPY app.py .

# Expose port the app listens on
EXPOSE 5000

# Run with gunicorn, binding to 0.0.0.0:5000, single worker for small apps
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "8"]