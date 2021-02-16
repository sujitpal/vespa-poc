#!/bin/bash
container_name=`docker ps | grep -v CONTAINER | rev | cut -d" " -f1 | rev`
docker exec -it vespa /bin/bash

