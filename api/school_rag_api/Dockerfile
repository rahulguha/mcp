
# Use a slim Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip (simpler and more reliable in slim images)
RUN pip install uv
RUN pip install --no-cache-dir python-dotenv==1.0.1

# Copy uv configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen

# Copy the entire project, including data and website_content folders
COPY . .

# Expose port 3200
EXPOSE 3200

# Run the FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "school_chat_api:app", "--host", "0.0.0.0", "--port", "3200"]
