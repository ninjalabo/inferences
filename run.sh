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

# save results to output.json
{
  echo "{"
  echo "  \"accuracy\": $accuracy,"
  echo "  \"size\": $model_size,"
  echo "  \"speed\": $speed"
  echo "}"
} > output.json
