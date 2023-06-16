FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS=ignore
ENV POETRY_VIRTUALENVS_CREATE=false
EXPOSE 8080/tcp
RUN apt-get update -y --no-install-recommends
RUN apt-get install -y --no-install-recommends \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    gcc `# для cryptography`
RUN pip install --user poetry==1.3.2
RUN pip install certifi==2021.10.8
ENV PATH="${PATH}:/root/.local/bin"
RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install --no-interaction --no-ansi
COPY / /app/
RUN chmod +x entrypoint.sh
