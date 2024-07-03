#!/bin/sh

if [ $# -lt 3 ]; then
  echo "Usage: $0 <inference> <model_path> <data_path...>"
  exit 1
fi

inference=$1
model_path=$2
shift 2
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

# Check if accuracy, speed, and model_size are not empty
if [ -n "$accuracy" ] && [ -n "$speed" ] && [ -n "$model_size" ]; then
  # Update runtime_info.json
  temp_file=$(mktemp)
  jq ".results = {accuracy: $accuracy, size: $model_size, speed: $speed}" md/runtime_info.json > "$temp_file"
  mv "$temp_file" md/runtime_info.json
else
  echo "Error: Inference failed."
  [ -z "$accuracy" ] && echo "Accuracy is empty."
  [ -z "$speed" ] && echo "Speed is empty."
  [ -z "$model_size" ] && echo "Model size is empty."
  exit 1
fi
