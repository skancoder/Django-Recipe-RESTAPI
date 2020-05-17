# Django-Recipe-RESTAPI
python -m django --version

#### Build Docker Image
https://hub.docker.com/_/python

create docker file 
> docker build .

#### Build Docker Compose
create docker-compose.yml file
>docker-compose build

#### run commands
> docker-compose run app sh -c "django-admin.py startproject app ."

run app> run service name called app which is there in docker-compose

startproject app> app is a project name

.> location of the project

without docker: run: > django-admin.py startproject app .

#### travis CI
open travis CI and enable this git repo in travis CI
to tell trabis CI what to do every time we push code to git
#if the code fails then it will fail the build and sends email notification

.travis.yml
> language: python
> python:
>   - "3.8.3"
> services:
>   - docker 
> # command to install dependencies
> install:
>   - pip install -r requirements.txt
> # command to run tests
> script:
>   - docker-compose run app sh -c "python manage.py test && flake8"