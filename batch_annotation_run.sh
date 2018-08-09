#!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Annotating user: $line"
    sbatch -W annotation_run.sh $line
done < "$1"

