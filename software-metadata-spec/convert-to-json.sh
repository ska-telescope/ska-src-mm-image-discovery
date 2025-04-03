#!/bin/bash

#!/bin/bash

# Define an array of YAML files to be converted
yaml_files=(
  "software-metadata-spec/sample/jupyter-notebook/notebook.yaml"
  "software-metadata-spec/sample/oci-images/carta/carta.yaml"
  "software-metadata-spec/sample/oci-images/jupyter-notebook/canucs.yaml"
)

# Loop through each YAML file and convert it to JSON
for yaml_file in "${yaml_files[@]}"; do
  json_file="${yaml_file%.yaml}.json"
  yq -p yaml -o json "$yaml_file" > "$json_file"
done