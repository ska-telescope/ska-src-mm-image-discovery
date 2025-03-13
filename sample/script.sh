#!/bin/bash

yq -p yaml -o json sample/jupyter-notebook/notebook.yaml >  sample/jupyter-notebook/notebook.json

yq -p yaml -o json sample/oci-images/carta/carta.yaml >  sample/oci-images/carta/carta.json
yq -p yaml -o json sample/oci-images/jupyter-notebook/canucs.yaml >  sample/oci-images/jupyter-notebook/canucs.json



# software_metadata -> docker-container + jupyter-notebook