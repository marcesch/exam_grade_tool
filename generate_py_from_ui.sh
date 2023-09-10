#!/bin/bash

# Loop through .ui files in the ui/ folder
for ui_file in ui/*.ui; do
    # Extract the file name without extension
    base_name=$(basename "${ui_file%.*}")

    # Generate .py file path in the frontend/ folder
    py_file="frontend/${base_name}.py"

    # Run pyuic6 command
    pyuic6 -o "$py_file" "$ui_file"

    echo "Generated $py_file"
done