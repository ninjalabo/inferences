import subprocess
import json
import sys

def run_command(command, cwd=None):
    try:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}")
        print(e.stderr)
        exit(1)

def main(architecture):
    # Python inference
    run_command("./run.sh run.py md/model.pkl md/data/test")

    # Vanilla C inference
    run_command("docker run --rm -v $(pwd)/md:/root/md ninjalabo/compiler-export-models")
    run_command(f"./run.sh {architecture}/run md/model.bin md/data/test/*/*")

    # Quantized C inference 
    with open('md/runtime_info.json', 'r') as file:
        data = json.load(file)
        data['compression']['quantization'] = True
    with open('md/runtime_info.json', 'w') as file:
        json.dump(data, file, indent=4)
    run_command("docker run --rm -v $(pwd)/md:/root/md ninjalabo/compiler-export-models")
    run_command(f"./run.sh {architecture}/runq md/model.bin md/data/test/*/*")

if __name__ == "__main__":
    architecture = sys.argv[1]
    main(architecture)
