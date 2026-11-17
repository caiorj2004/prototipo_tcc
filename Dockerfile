FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=7860
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import os,urllib.request as u; u.urlopen('http://localhost:'+os.environ.get('PORT','7860')+'/')" || exit 1

# Em produção (K8s): gunicorn. Para desenvolvimento local: python app.py
CMD ["sh", "-c", "gunicorn app:server --bind 0.0.0.0:${PORT} --workers 2 --timeout 120"]
