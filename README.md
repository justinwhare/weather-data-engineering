# Weather Data Dashboard

The purpose of this project is to obtain live weather data and analyze and report it on a dashboard.
 
This project was done to develop data engineering skills performing ELT tasks and orchestration. This repository contains the code to set up the backend for these services:
- **airflow**: orchestration and data flow
- **dbt**: data transformation and DAG execution
- **postgres**: RDBMS storing weather data
- **superset**: data visualization

The initialization of these services is done through the use of a `docker-compose.yaml` file.

The weather data for this project was obtained from the [WeatherStack API](https://weatherstack.com/).

