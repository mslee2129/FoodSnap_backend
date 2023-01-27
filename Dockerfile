FROM python:3.10.8

# Setting working directory
WORKDIR /code

# Install python packages
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Copy code
COPY ./app /code/app

# Run flask application
ENV FLASK_APP=app/api/endpoint.py
CMD flask run --port "$PORT"
