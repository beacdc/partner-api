FROM python:3.7.9-slim

RUN mkdir /temp

# Install Requirements
WORKDIR /temp
ADD requirements.txt /temp
ADD requirements-lint.txt /temp
ADD requirements-dev.txt /temp
RUN pip install -r /temp/requirements-dev.txt

# Expose port 3000
EXPOSE 3000

# Deploy application
RUN mkdir /app
WORKDIR /app

CMD [ "python", "-B", "main.py" ]
