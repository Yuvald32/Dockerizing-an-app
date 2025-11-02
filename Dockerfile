FROM python:3.13-slim AS runtime

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV TZ=Asia/Jerusalem

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/

RUN useradd -m appuser
USER appuser

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5001/healthz')" || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]