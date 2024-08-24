#FROM python:3.5.2
FROM python:3.9 as build

# RUN groupadd web
# RUN useradd -d /home/python -m python

# Env vars for Datadog Instrumentation
ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL} 
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}
# ENV DD_SERVICE="fruits-app"
# ENV DD_ENV=""
# ENV DD_VERSION="0.2.1"

# RUN mkdir /home/python
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -U pip -r requirements.txt
COPY app.py .
RUN mkdir src
COPY src/db.py ./src
COPY src/__init__.py ./src

#EXPOSE 80
#ENTRYPOINT [ "sleep", "10000" ]
CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["flask", "run"]
