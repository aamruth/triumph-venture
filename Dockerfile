FROM python:3.8.12-buster

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then only, install taxifare!
COPY triumph-venture triumph-venture
COPY setup.py setup.py
RUN pip install .

# We already have a make command for that!
COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn triumph-venture.api.main:app --host 0.0.0.0 --port $PORT