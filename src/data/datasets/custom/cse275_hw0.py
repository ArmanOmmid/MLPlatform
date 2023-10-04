
import os
import numpy as np

import torchvision.transforms as T

from src.data.datasets import _Dataset

class CSE275_HW0(_Dataset):
    
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

        input, target = super().transform(input, target)

        return input, target
    
    def set_transforms(self):
        """
        Set the FUNDEMENTAL transforms for this dataset
        """
        self.input_transform = T.Compose([
            T.ToTensor(),
        ])
        self.target_transform = T.Compose([
            T.ToTensor(),
        ])
