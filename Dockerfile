# set base image (host OS)
FROM python:3.10

# set the working directory in the container
WORKDIR /code

# install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy the dependencies file to the working directory
COPY . .

ENTRYPOINT [ "python3", "main.py" ]