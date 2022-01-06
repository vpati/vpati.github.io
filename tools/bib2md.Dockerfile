FROM python:3.7

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git

RUN pip install pipenv

WORKDIR /
COPY Pipfile /
COPY bib2md.py /
COPY bib2md.j2 /
RUN pipenv install
