#!/bin/bash
docker info | grep "Total Memory"
echo "Checking if server is up, if response not 200 OK wait a while and retry"
docker exec vespa bash -c "curl -s --head http://localhost:19071/ApplicationStatus"
