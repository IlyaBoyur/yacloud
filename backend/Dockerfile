FROM python:3.11.0-slim
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore
ENV POETRY_VIRTUALENVS_CREATE false
ENV PATH "${PATH}:/root/.local/bin"

# Expose port 8080
EXPOSE 8080/tcp

# Install necessary dependencies
RUN apt-get update -y --no-install-recommends; \
    apt-get install -y --no-install-recommends \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    gcc `# для cryptography`; \
    pip install --user poetry==1.6 && pip install certifi==2021.10.8

# Set working directory for the application
WORKDIR /app/

# Copy just the dependencies installation from the current directory to the Docker image
COPY pyproject.toml poetry.lock ./

# Install necessary dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the current directory contents into the container
COPY . .

# Give necessary permissions to entrypoint
RUN chmod +x entrypoint.sh
