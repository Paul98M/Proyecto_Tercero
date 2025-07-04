FROM python:3.11-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD [ "python", "-m", "flask", "--app=my-app/run", "--debug", "run", "--host=0.0.0.0"]
