#!/bin/sh

if [ $# -lt 4 ]; then
  echo "Usage: $0 <image_name> <inference> <model_path> <data_path...>"
  exit 1
fi

image_name=$1
inference=$2
model_path=$3
shift 3
data_paths="$@"

if [ ${inference##*.} = py ]; then
  command="python $inference"
else
  command=$inference
fi

start_time=$(date +%s)
accuracy=$($command $model_path $data_paths)
end_time=$(date +%s)
speed=$((end_time - start_time))

if [ "$(uname)" = "Darwin" ]; then
  model_size=$(stat -f%z $model_path)
else
  model_size=$(stat -c%s $model_path)
fi

# Update output.json file for the specified image
temp_file=$(mktemp)
jq "map(if .image == \"$image_name\" then . + {results: {accuracy: $accuracy, size: $model_size, speed: $speed}} else . end)" md/output.json > "$temp_file"
mv "$temp_file" md/output.json
