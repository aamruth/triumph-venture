FROM python:3.10.6-buster

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then only, install triumph-venture!
COPY triumphventure triumphventure
COPY setup.py setup.py
RUN pip install .

CMD uvicorn triumphventure.api.main:app --host 0.0.0.0 --port $PORT