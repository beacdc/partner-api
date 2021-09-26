FROM python:3.7.9-slim

RUN mkdir /temp

# Install Requirements
WORKDIR /temp
ADD requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

# Expose port 3000
EXPOSE 3000

# Deploy application
RUN mkdir /app
ADD src /app
ADD infrastructure/bin/app.sh /app/app.sh
WORKDIR /app

CMD ./app.sh