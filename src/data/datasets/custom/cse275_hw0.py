
import os
import numpy as np
from torch.utils.data import Dataset

class CSE275_HW0(Dataset):
    
    def __init__(self, config):
        super().__init__()

        self.mode = config.mode
        
        datapath = os.path.join(config.path.data, f"{config.mode}.npz")

        if config.mode == "train":
            self.inputs, self.targets = np.load(datapath)
        elif config.mode == "test":
            self.inputs, self.targets = np.load(datapath), None # No labels in test
    
        self.input_transform = None
        self.target_transform = None

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        input, target = super().__getitem__(index)

        if self.input_transform:
            input = self.input_transform(input)

        if self.target_transform:
            target = self.target_transform(target)
            
        return input, target
    
    def set_transforms(self, input_transform=None, target_transform=None):
        self.input_transform = input_transform
        self.target_transform = target_transform
