
import os
import torch
import torchvision
import torchvision.transforms as T
from torch.utils.data import Dataset

from src.data.datasets import _Dataset

def get_standard_dataset(config, download: bool = False):
    """

    Available Datasets
        CIFAR10 - 10 classes
        CIFAR100 - 100 classes
        MNIST - 10 classes
        FashionMNIST - 10 classes
        StanfordCars - 196 classes
        Food101 - 101 classes (huge dataset)
        * Caltech256 - 256 classes (needs special consideration, not working)

    Apply Transforms with dataset.transform = transforms

    """
    assert config.mode in ["train", "test"], "config.mode must be in ['train', 'test']"

    datapath = os.path.join(config.path.data, config.dataset, config.mode)
    Dataset_Class = getattr(torchvision.datasets, config.dataset)
    # dataset = Dataset_Class(datapath, download=download, train=config.mode)
    dataset = generate_derived_class(Dataset_Class)(datapath, download=download, train=config.mode)
    return dataset

def generate_derived_class(base_class: type=Dataset):
    """
    Dynamic Inheritance. 
    """

    class StandardDataset(base_class, _Dataset):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.base_class = base_class

        def __getitem__(self, index):
            input, target = super(self.base_class).__getitem__(index)

            input, target = super(_Dataset).transform(input, target)
                
            return input, target
        
        def set_transforms(self):
            """
            Set the FUNDEMENTAL transforms for this dataset
            # ToTensor handles PIL and Numpy Arrays
            # It also scales their 255 values to [0, 1]
            # Also ensure channels dimension is the first dimension
            """
            self.input_transform = T.Compose([
                T.ToTensor(),
            ])
            self.target_transform = T.Compose([
                T.ToTensor(),
            ])

    StandardDataset.__name__ = f"StandardDataset::{base_class.__name__}"

    return StandardDataset
