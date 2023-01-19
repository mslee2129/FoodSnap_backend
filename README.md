# Image recognition-based calorie tracker

## Description

Imagine that you could show a dish to a machine learning algorithm and it would come back to you with the number of calories that it contained? In this project we have developed an image recognition-based calorie tracker.

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