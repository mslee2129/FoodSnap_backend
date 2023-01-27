FROM python:3.10

# Setting working directory
WORKDIR /code

# # Install python packages
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install pipenv


# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# # Copy app code
# COPY ./*.py /code/
# COPY ./app /code/app

# CMD ["gunicorn", "--config", "gunicorn_config.py", "main:app"]
