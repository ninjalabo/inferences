import subprocess
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
    run_command("./run.sh run.py md/model.pkl data/test")

    # Vanilla C inference
    run_command("docker run --rm -v $(pwd)/md:/root/md ninjalabo/compiler-export-vanilla")
    run_command(f"./run.sh {architecture}/vanilla/run md/model.bin data/test/*/*")
    
    # Dynamically quantization C inference
    run_command("docker run --rm -v $(pwd)/md:/root/md ninjalabo/compiler-export-dq")
    run_command(f"./run.sh {architecture}/dq/runq md/model.bin data/test/*/*")
    
    # Static quantization C inference
    run_command("docker run --rm -v $(pwd)/md:/root/md -v $(pwd)/data:/root/data ninjalabo/compiler-export-sq")
    run_command(f"./run.sh {architecture}/sq/runq md/model.bin data/test/*/*")

if __name__ == "__main__":
    architecture = sys.argv[1]
    main(architecture)
