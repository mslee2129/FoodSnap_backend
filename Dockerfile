FROM python:3.10.8

# Setting working directory
WORKDIR /code

# Install python packages
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

# Copy code
COPY ./app /code/app

# Run flask application
CMD gunicorn --bind :$PORT app.api.endpoint:app