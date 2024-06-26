FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ \
    "streamlit", \
    "run", \
    "src/app/streamlit_app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0" \
]
