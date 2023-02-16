FROM python:3.10.8

# Set working directory
WORKDIR /code

# Copy ML model
COPY *.pt .

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy code for application
COPY ./app /code/app

# Run flask application
CMD gunicorn --bind :$PORT app.api.endpoint:app