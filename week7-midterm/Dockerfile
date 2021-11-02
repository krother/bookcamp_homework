FROM agrigorev/zoomcamp-model:3.8.12-slim

COPY Pipfile /app
COPY Pipfile.lock /app

RUN pip install pipenv
RUN pipenv install --system --deploy

RUN mkdir /app/static
RUN mkdir /app/static/uploads
RUN mkdir /app/templates

COPY app.py /app
COPY pixpro.py /app
COPY static/style.css /app/static
COPY templates/main.html /app/templates
COPY templates/result.html /app/templates

CMD ["pipenv", "run", "gunicorn", "app:app"]
