#FROM ubuntu:16.04
FROM ubuntu:latest
RUN echo Updating existing packages, installing and upgrading python and pip.
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN pip3 install --upgrade pip
RUN echo Copying the Flask app into a app directory.
COPY ./app /app
WORKDIR /app
RUN echo Installing Python packages listed in requirements.txt
RUN pip3 install -r ./requirements.txt
RUN echo Starting python and starting the Flask app...
ENTRYPOINT ["python3"]
CMD ["run.py"]
