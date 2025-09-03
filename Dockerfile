FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app.py /app

EXPOSE 5001
ENV AWS_DEFAULT_REGION="us-east-1"

CMD ["python", "app.py"]
