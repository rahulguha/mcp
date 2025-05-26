

# Use Python 3.13 slim image as required by pyproject.toml
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock /app/

# Sync dependencies from uv.lock
RUN uv sync --frozen

# Copy application code
COPY . /app/

# Expose port 8080
EXPOSE 8080

# Run FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "school_chat_api:app", "--host", "0.0.0.0", "--port", "8080"]