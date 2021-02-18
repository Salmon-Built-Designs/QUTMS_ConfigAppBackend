# QUTMS_ConfigApp Backend

<!-- ![ConfigApp](/wiki/banner.png) -->

## ConfigApp Backend
This is the backend for ConfigApp, a web-based app used to process and view car log data. Processed log files are stored and made available for later reference. The aim of the app is to unify data recorded from track days and make it avaiable in a central location.

The backend is built on Flask, a micro web framework that handles requests from the frontend. The backend is deployed in a Docker-compose container, together with the React based frontend and a Postgres database.


## Getting Started
The backend is built using [Conda](https://docs.conda.io/en/latest/miniconda.html) and must be installed first. Then the project environment  can be created from the included environment.yml file and then activated. The Flask app can then be run.

```shell
conda env create -f environment.yml
conda activate cfback
flask create-db
flask run
```

All commands must be run from the base directory. Go [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) for more information on conda and conda environments. If the environment is activated correctly, you will see (cfback) at the start of your terminal/shell line (See below).

```shell
(cfback) QUT_PC:QUTMS_ConfigAppBackend user$ 
```

When running the backend independent of the frontend and Docker, the app will create an export folder in the base directory to dump processed data and a test database in src/backend.

## Project Layout
Refer below for a rough diagram showing the workings of ConfigApp.

![Project Diagram](/ConfigApp_overview.png)

## Docker Deployment
Docker and Docker-compose are used to deploy ConfigApp. Download Docker Desktop (windows & mac) or on linux Docker and Docker-compose. 

```shell
docker-compose up --build
```

The docker-compose.yml file is setup to build the backend container locally and pull the frontend from the dockerhub. Be sure to include the build command or it won't work.

### Editing the Frontend / UI (Typescript & React)

Go to the frontend Git for more information.

## Available Scripts

There have been a number of command line functions attached to the Flask app to facility database management.

If running in a Docker container, you must first open up an interactive shell from inside it.
```shell
docker exec -ti cfh_backend /bin/bash
conda activate cfback
```

In the project directory, you can run:

### `flask run`

Runs the app in the development mode using the environment variables declared in the environment.yml file. To test functionality use curl commands (See below).

### `flask create-db`

Creates a new database for storing log and user information. If running in Docker-compose, it will create a database in the Postgres DB volume.

### `flask clear-db`

Drops all tables from the database after confirmation. Use with caution.

### `flask list-logs`

Lists all the log entries currently stored in the database.

(More commands to be added as development continues.)

## Want to Get Involved?

Studying at QUT? Contact us at qutmotorsport.team@gmail.com or [visit our website](https://www.qutmotorsport.com/) for details on how you can get involved.