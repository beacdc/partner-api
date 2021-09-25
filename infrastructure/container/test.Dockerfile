FROM python:3.7.9-slim

RUN mkdir /temp

# Install Requirements
WORKDIR /temp
ADD requirements.txt /temp
ADD requirements-test.txt /temp
RUN pip install -r /temp/requirements-test.txt

# Deploy application
RUN mkdir /app
WORKDIR /app

CMD [ "ptw" ]
