# set base image (host OS)
FROM python:3.10

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY . .

# # install dependencies
# RUN pip install -r ./code/requirements.txt

ENTRYPOINT [ "python3", "main.py" ]