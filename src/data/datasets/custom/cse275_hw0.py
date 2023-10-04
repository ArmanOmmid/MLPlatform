
import os
import numpy as np
from torch.utils.data import Dataset

class CSE275_HW0(Dataset):
    
    def __init__(self, config):
        super().__init__()

        self.mode = config.mode
        
        datapath = os.path.join(config.path.data, type(self).__name__, f"{config.mode}.npz")

        print("Loading from: ", datapath)
        npz = np.load(datapath)

        self.inputs, self.targets = npz["images"], npz["edges"]
        self.input_transform = None
        self.target_transform = None

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        input, target = self.inputs[index], self.targets[index]

        if self.input_transform:
            input = self.input_transform(input)

        if self.target_transform:
            target = self.target_transform(target)
            
        return input, target
    
    def set_transforms(self, input_transform=None, target_transform=None):
        self.input_transform = input_transform
        self.target_transform = target_transform
