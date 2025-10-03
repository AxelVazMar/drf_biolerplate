#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME="django"

# Ejecutar bash dentro del contenedor
docker exec -it $CONTAINER_NAME /bin/bash