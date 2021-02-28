# vespa-poc
Small Proof of Concept to familiarize myself with [vespa.ai](https://vespa.ai/) functionality

## Usage Instructions

1. Clone the vespa-engine/sample-apps repository.
   '$ git clone https://github.com/vespa-engine/sample-apps.git'
2. Copy the contents of `src/` to a subfolder given by your application name (say `vespa-poc`)
   ```
   $ cd ../sample-apps
   $ mkdir vespa-poc
   $ cd -
   $ cp -r src ../sample-apps/
   ```
3. Set the value of SAMPLE_APPS_DIR and APP_NAME in all the files in `bash-scripts` (alternative is to pass them in via command line but this is one time for an application).
   ```
   SAMPLE_APPS_DIR=$HOME/sample-apps
   APP_NAME=vespa-poc
   ```

You can then `launch.sh` to start a docker instance the first time, `status.sh` to check on the readiness of the vespa engine, `deploy.sh` to deploy the vespa-poc configuration to the vespa engine, `start.sh` and `stop.sh` to start and stop vespa thereafter, and `terminate.sh` to remove the vespa container once you are done.

The `python-scripts/index/prepare-and-load-index.py` parses a CORD-19 dataset (you have to download from AllenAI and untar it locally), and extracts metadata (`cord_uid`, `title`, and `abstract`) and the SPECTER embedding and writes it to the `vespa-poc` application.

The `python-scripts/search/` contains two scripts, one to do a simple text search, and another to find more like this (MLT) given an input document.

Together, this represents (for me) a MVP (minimal viable "product") to get started with Vespa.

In addition, the `python-scripts/demo/` directory contains a [Streamlit](https://www.streamlit.io/) dashboard to demonstrate the functionality (search and MLT) to human users, and a [FastAPI](https://fastapi.tiangolo.com/) service to allow batch consumption of the service via script. FastAPI provides a built-in Swagger UI, which is very convenient to figure out how to use the API. The additional libraries necessary for running these two services are listed in [python-scripts/requirements.txt](https://github.com/sujitpal/vespa-poc/blob/main/python-scripts/requirements.txt).

To start the Streamlit dashboard, navigate to the `demo` directory and run the following command. This will start the Streamlit service on port 8501 and you can access the dashboard on your browser at http://localhost:8501.

```
$ streamlit run dashboard.py
```

To start the FastAPI service, navigate to the same `demo` directory and run the following command. This will start the FastAPI service on port 8000 and you can access the Swagger UI at http://localhost:8080/docs.

```
$ uvicorn api:app --reload
```


