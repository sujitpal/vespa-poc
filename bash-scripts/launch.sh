#!/bin/bash
SAMPLE_APPS_DIR=$HOME/sample-apps

docker run --detach --name vespa --hostname vespa-container --volume $SAMPLE_APPS_DIR:/vespa-sample-apps --publish 8080:8080 vespaengine/vespa

