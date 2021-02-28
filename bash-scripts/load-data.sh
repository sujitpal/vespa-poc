#!/bin/bash
APP_NAME=vespa-poc
JSON_INPUT_DIR=$HOME/sample-apps/$APP_NAME/data

INPUT_FILE=$1
docker exec vespa bash -c 'java -jar /opt/vespa/lib/jars/vespa-http-client-jar-with-dependencies.jar --verbose --file $JSON_INPUT_DIR/$INPUT_FILE --host localhost --port 8080'
