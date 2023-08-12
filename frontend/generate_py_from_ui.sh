#!/bin/bash

# Loop through .ui files
for ui_file in *.ui; do
    # Extract the file name without extension
    base_name="${ui_file%.*}"

    # Generate .py file name
    py_file="${base_name}.py"

    # Run pyuic6 command
    pyuic6 -o "$py_file" "$ui_file"

    echo "Generated $py_file"
done
