#!/bin/bash
echo "--- Total Memory Available ---"
sudo docker info | grep "Total Memory"
echo "--- Config Server State ---"
sudo docker exec vespa bash -c "curl -s --head http://localhost:19071/ApplicationStatus"
echo "--- Cluster State ---"
sudo docker exec vespa bash -c "/opt/vespa/bin/vespa-get-cluster-state"
echo "--- Proton Status ---"
sudo docker exec vespa bash -c "/opt/vespa/bin/vespa-proton-cmd --local getProtonStatus"
