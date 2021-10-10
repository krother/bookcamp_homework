FROM agrigorev/zoomcamp-model:3.8.12-slim

COPY Pipfile /app
COPY Pipfile.lock /app

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY model1.bin /app
COPY dv.bin /app
COPY app.py /app
COPY predict.py /app

CMD ["pipenv", "run", "gunicorn", "app:app"]
