#!/bin/bash
# script to recursively go through all notebooks and clean the output cells
find .. -name "*.ipynb" -exec jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {} \;