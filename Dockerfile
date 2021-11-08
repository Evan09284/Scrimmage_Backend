FROM python:3.8-slim-buster

WORKDIR /app/

COPY . /app/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ARG REDIS_URL
ARG META_KEY

ENV FLASK_ENV=development
ENV REDIS_URL=$REDIS_URL
ENV META_KEY=$META_KEY

RUN echo $REDIS_URL

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
