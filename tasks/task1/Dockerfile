FROM python:3.6.8-jessie

COPY requirements.txt /requirements.txt

# will be overwriten should `docker run` pass a proper env
ENV EXECUTION_ID 111111

# they HAVE to match the name of jupyter's kernel
RUN pip install virtualenv \
    && virtualenv -p python3 airflow_jupyter \
    && /bin/bash -c "source /airflow_jupyter/bin/activate" \
    # change the url to reflect your local ip or wherever you setup your pypi server.. 127.0.0.1 doesn't work
    && pip install -i http://palehorse.lan:8011 --trusted-host palehorse.lan -r /requirements.txt \
    && ipython kernel install --user --name=airflow_jupyter \
    && mkdir notebook \
    && mkdir notebook/output

COPY code.ipynb ./notebook/code.ipynb
COPY params.yaml ./notebook/params.yaml

WORKDIR notebook
ENTRYPOINT ["python", "-c", "from papermill_runner import PapermillRunner;PapermillRunner().run()"]