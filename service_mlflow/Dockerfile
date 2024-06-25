FROM python:3.10-slim

RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y procps
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip install --disable-pip-version-check -r requirements.txt

EXPOSE ${MLFLOW_CONTAINER_PORT}
COPY ./scripts/run_mlflow.sh run_mlflow.sh
CMD ["/bin/bash", "run_mlflow.sh"]