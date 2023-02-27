# Sample E-learning App

[Complete application image will go here]

## Overview

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.

### Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Additional Details](#additional-details)
- [Application Details](#application-details)
- [Testing It Locally](#testing-it-locally)


## Features

- Lorem Ipsum is simply dummy text
- Lorem Ipsum is simply dummy text

## Technologies Used

- Lorem Ipsum is simply dummy text
- Lorem Ipsum is simply dummy text

## Additional Details

| Db Schema Design | UI Design   | Deployment | Contributors    | Tests    |
| --------------- | ------   | ---------- | --------------- | -------- |
| [drawSQL](https://drawsql.app/teams/gitau-harrison/diagrams/sample-elearning-app)        | [Figma](https://www.figma.com/proto/iHXb2ynMTIyelCqlVAk30u/Lean-Sigma?node-id=1%3A2&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=1%3A2) | [Render](https://somasoma.onrender.com)     | [GitHub](https://github.com/GitauHarrison/sample-elearning-app/graphs/contributors)        | [Tests](test_app.py) |


## Application Details



## Testing It Locally

- Clone this repo:

    ```python
    $ git@github.com:GitauHarrison/sample-elearning-app-flask.git
    ```
- Change directory into the cloned repo:

    ```python
    $ cd sample-elearning-app-flask
    ```
- Create and activate a virtual environment

    ```python
    # Using virtualenvwrapper
    $ mkvirtualenv venv

    # Normal way
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

- Install needed dependancies:

    ```python
    (venv)$ pip3 install -r requirements.txt
    ```

- Add and update environment variables in a `.env` file as seen in `.env-template`:

    ```python
    (venv)$ cp .env-template .env
    ```

- Start the flask server:

    ```python
    (venv)$ flask run
    ```

- Check the application in your favourite browser by pasting http://127.0.0.1:5000.