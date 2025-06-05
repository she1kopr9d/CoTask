FROM python:3.12
WORKDIR /usr/src/app
COPY requirements/prod.txt .
RUN pip install -r prod.txt
COPY . .