
FROM python:3.10.14



EXPOSE $PORT
#ENV PORT=8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .


# Update base libs before we install other libs
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip python3-wheel


# tensorflow need this lib and it is different base on OS.
RUN apt-get install -y libhdf5-dev


# install pipenv 
RUN pip install pipenv

# Install pipenv lib with Pipfile.lock Hash
RUN pipenv install --system --deploy
#RUN pipenv install

CMD ["python","main.py"]