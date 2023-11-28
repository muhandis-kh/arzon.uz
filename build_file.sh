#!/bin/bash

# Update pip
echo "Updating pip..."
python3.9 pip install -U pip

# Install dependencies

# build_files.sh
pip install -r requirements.txt