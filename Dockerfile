FROM python:3.10

# Setting working directory
WORKDIR /code

# Install python packages
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Copy app code
COPY ./app /code/app

# Run flask application
CMD ["flask", "--app", "app.api.endpoint", "run", "--port", $PORT]
