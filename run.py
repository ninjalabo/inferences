import os
import torch
import numpy as np
import struct
import sys
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from contextlib import redirect_stdout

class TensorDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.classes = sorted(os.listdir(root_dir))
        self.file_paths = []
        self.labels = []
        for label in self.classes:
            label_dir = os.path.join(root_dir, label)
            files = os.listdir(label_dir)
            for file in files:
                self.file_paths.append(os.path.join(label_dir, file))
                self.labels.append(int(label))

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        with open(self.file_paths[idx], "rb") as f:
            nch, h, w = 3, 224, 224
            tensor = torch.tensor(struct.unpack("f"*nch*h*w, f.read())).view(nch,h,w)
        label = self.labels[idx]
        return tensor, label

def run_python(model_path, dir_path):
    # get file paths of images and their labels
    files = []
    label_count = np.zeros(10, dtype=int)
    for label in range(10):
        sd_path = os.path.join(dir_path, str(label))
        f_paths = [os.path.join(sd_path, file) for file in os.listdir(sd_path)]
        label_count[label] = len(f_paths)
        files += f_paths

    # run Python inference
    learn = torch.load(model_path, map_location='cpu')
    learn.model.eval()
    test_dl = DataLoader(TensorDataset("data/test/"), batch_size=32, num_workers=os.cpu_count())
    with open(os.devnull, 'w') as f, redirect_stdout(f): # suppress stdout
        _, accuracy = learn.validate(dl=test_dl)
        accuracy = 100 * accuracy

    return accuracy

def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py <model> <data directory>")
        return
    
    model_path = sys.argv[1]
    dir_path = sys.argv[2]

    result = run_python(model_path, dir_path)
    print(result)

if __name__ == "__main__":
    main()
