[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Wine Store

This project is an API for a wine store. It is built with Django and Django Rest Framework. The project implement the basic logic in a e-commerce store (User authentication, User registration, User profile, List and get wines, List and get reviews for a wine, Create, update and delete reviews for a wine, Get, add, update and delete items in a shopping cart, Place an order). This project is 65% complete.

## Table of Contents

- [Wine Store](#wine-store)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Built With](#built-with)
  - [Features](#features)
  - [Settings](#settings)
  - [Acknowledgements](#acknowledgements)

## Overview

The project use [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django/) as starting point. The project use Docker and docker-compose for development and deployment. Also use [`AllAuth`](https://github.com/pennersr/django-allauth) for and [`dj_auth_rest`](https://github.com/iMerica/dj-rest-auth) for API authentication.

The main project features are features:

- [x] User authentication 100%
- [ ] User registration
- [ ] User profile
- [ ] List and get wines
- [ ] List and get reviews for a wine
- [ ] Create, update and delete reviews for a wine
- [ ] Get, add, update and delete items in a shopping cart
- [ ] Place an order

### End points

This project has the following end points:

#### User

- [ ] `/api/authentication/` - List all users

#### Products

- [ ] `/api/wines/` - List all wines
- [ ] `/api/wines/<id>` - Get a wine by id
- [ ] `/api/wines/<id>/reviews/` - List all reviews for a wine

## Built With

## Features

## Settings

## Acknowledgements
