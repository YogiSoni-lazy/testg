# Reporting API Server

## Endpoints

### Health Check

  Health check.

* **URL**

  `/v1/healthz`

* **Method:**

  `GET`

* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200
    **Content:** `{'health': 'ok'}`


### Save Report

  Saves the json data about a report.

* **URL**

  `/v1/report`

* **Method:**

  `POST`

* **URL Params**

  None

* **Data Params**

  JSON object

* **Success Response:**

  * **Code:** 201
    **Content:** Empty
    **HTTP Headers:**
      * Location

* **Error Responses:**

  * **Code:** 400

### Get Report

  Returns json data about a report.

* **URL**

  `/v1/report/:id`

* **Method:**

  `GET`

* **URL Params**

  **Required:**

  `id=[int]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200
   **Content:** `{'key': 'value', ...}`

* **Error Responses:**

  * **Code:** 404

## Installation

The Reporting API is a Python application with Flask so, in order to run in your local machine you need Python + some libraries.

Execute the following command to install all the required libraries:

```shell script
pip install -r requirements.txt
```

To persist data the server uses `sqlite` and the database is stored in the `data` folder.

Execute the following command to initialize the required database and tables:

```shell script
cd ./data && ./initialize-data.py
```

## Running the Reporting API Server in local

The Reporting API Server can be started with the `reporting-server.sh` script. By default opens a web server running in port 5000 in debug mode.
