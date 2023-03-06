# FoodSnap: Image recognition-based calorie tracker

## Description

Imagine that you could show a dish to a machine learning algorithm and it would come back to you with the number of calories that it contained? In this project we have developed an image recognition-based calorie tracker.

This project contains the python back-end and API endpoint for the FoodSnap application.

## Set up

In this project we use Python version `3.10.8` and Pipenv for managing virtual environments (see full documentation [here](https://pipenv-fork.readthedocs.io/en/latest/basics.html)).

The local environment (for development) can be set up by running [`setup.sh`](setup.sh):
```
bash setup.sh
```

This assumes that `pipenv` is already installed, if not then uncomment out the section for installing this with `pip` (for Mac users you can also use `brew`) or simply run:
```
pip install pipenv
```

There are a number of environment variables used throughout this project - these should be stored in a local `.env` file. First copy the [`.env.example`](.env.example) file into `.env` and then add the variable values. These will be loaded in when you activate your virtual environment.
```
cp .env.example .env
```

### Virtual Environment

Creat virtual environment and install dependencies listed in [`Pipfile`](Pipfile) (including `dev` dependencies):
```
pipenv install --dev
```

Activate environment:
```
pipenv shell
```

Exit environment:
```
deactivate
```

Delete environment:
```
pipenv --rm
```

Installing a new library (and updating [`Pipfile`](Pipfile) and [`Pipfile.lock`](Pipfile.lock)):
```
pipenv install library-name
```

## Execution

Prerequisites:
* Download a service account key as JSON file from GCP which is required for using the Vision API
* Ensure environment variables are set in `.env` (and set `GOOGLE_APPLICATION_CREDENTIALS` to the path where the service account key is located)
* Download the latest YOLO model from Cloud Storage (`gs://food-snap-artefacts/models/latest/model.pt`) and keep it in the root folder
* Activate the virtual environment

Run server:
```
flask --app app.api.endpoint --debug run
```

Make `POST` request with image stored locally (for example if you had an image called `omelette.jpg`):
```
curl -F file=@omelette.jpg "http://127.0.0.1:5000/"
```

You should see a response such as:
```
{
  "model_code": "YOLO_USE_PLATE_SIZE",
  "results": [
    {
      "label": "Omelette",
      "nutrition": {
        "CHOCDF": 13.0,
        "ENERC_KCAL": 632.6,
        "FAT": 48.8,
        "FIBTG": 2.4,
        "PROCNT": 35.2
      },
      "weight": 392.7
    }
  ],
  "status": "success"
}
```