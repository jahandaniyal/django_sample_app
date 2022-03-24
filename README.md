# Django Sample App
## Sample application for CRUD APIs

## Features

[![CircleCI](https://img.shields.io/circleci/build/github/jahandaniyal/django_sample_app/main?style=plastic)](https://circleci.com/gh/jahandaniyal/django_sample_app)

- Django App to implement CRUD operations for  **User**, **Usage** and **UsageTypes** table
- JWT Authentication using [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- Two User Access Control levels:
     - Admin or SuperUser
     - All other Users
- Unittest written using [pytest](https://docs.pytest.org/en/7.0.x/#)
- Local Build System and Dockerized Container
- Support for pagination, sorting and filter by time range
- OpenApi Spec generated and documented in *api_doc.html*

## Pre-requisites
- [Python 3.9+](https://docs.python.org/3.9/)
- [pip](https://pip.pypa.io/en/stable/installation/)
-  [Docker](https://docs.docker.com/get-docker/)
-  **Make** for building the project locally on Linux (tested on Ubuntu 20.04)

## Building Locally (Tested on Ubuntu)
- `git clone https://github.com/jahandaniyal/django_sample_app` - Clone this repository.
- `make build` - Execute this command on a linux terminal.
This will install all dependencies in a virtual environment and make all migrations to the data base.

## Running Locally
- `make run` - To run the web application in localhost
- `make test` - Runs pytest suite for the entire project
- `make clean` - Clears all environment variables and temporary files.

## Running in Docker Container
- `docker-compose up --build web` - For running the Web Application
- `docker-compose up --build test` - For running the Pytest suite.

## Nice to haves - Production Environment
- This was a small implementation, however to make the project scale-up more features needs to implemented.
- For example using Nginx & uWSGI for django and web server.
- Standard database like postgreSQL.
- Kubernetes Deployment in AWS or GCP.
- Datadog integration

**Time Spent** - ~6 hours

