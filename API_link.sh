#!/bin/bash
source=$1
atlasname=$2
atlasproject=$3
segpath=$4
token=$5
curl \
  -F url="$source" \
  -F atlasName="$atlasname" \
  -F atlasLabelSet=freesurfer.json \
  -F atlasProject="$atlasproject" \
  -F atlas=@$segpath \
  -F token=$token \
     https://brainbox.pasteur.fr/mri/upload