ARG IMAGE_NAME="quay.io/astronomer/astro-runtime:4.2.4-base"
FROM ${IMAGE_NAME}

USER root
RUN apt-get update -y && apt-get install -y git

COPY setup.cfg ${AIRFLOW_HOME}/astronomer_providers/setup.cfg
COPY pyproject.toml ${AIRFLOW_HOME}/astronomer_providers/pyproject.toml

RUN pip install -e "${AIRFLOW_HOME}/astronomer_providers[all,tests,mypy]"
USER astro
