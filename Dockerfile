FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/
COPY tests/ tests/

# Install the project
RUN pip install --no-cache-dir -e .

# Install Playwright dependencies
RUN pip install playwright && playwright install --with-deps chromium

CMD ["autosocial"]
