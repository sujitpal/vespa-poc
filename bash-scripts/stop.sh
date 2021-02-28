#!/bin/bash
docker exec vespa bash -c "/opt/vespa/bin/vespa-stop-services"
docker stop vespa

