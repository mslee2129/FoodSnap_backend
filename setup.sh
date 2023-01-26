#!/bin/bash

# colours
GREEN='\033[1;32m'
PURPLE='\033[1;35m'
NC='\033[0m'

echo -e "${GREEN}-----FoodSnap Backend Set Up-----${NC}\n"

# uncomment if you need to install pipenv
# pip install pipenv

echo -e "${PURPLE}Creating virtual environment...${NC}\n"
pipenv install --dev

echo -e "${PURPLE}Enabling pre-commits...${NC}\n"
pipenv run pre-commit install

echo -e "${PURPLE}Done!${NC}\n"