#!/bin/bash
SAMPLE_APPS_DIR=$HOME/sample-apps
APP_NAME=vespa-poc
DOCKER_APP_LOC=/vespa-sample-apps

docker exec vespa bash -c "/opt/vespa/bin/vespa-deploy prepare $DOCKER_APP_LOC/$APP_NAME/src/main/application/ && /opt/vespa/bin/vespa-deploy activate"

