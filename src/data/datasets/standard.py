
import os
import torch
import torchvision
from utils.config import Config
from torch.utils.data import Dataset

def get_standard_dataset(config: Config, download: bool = False):
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

    class StandardDataset(base_class):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.input_transform = None
            self.target_transform = None

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

    return StandardDataset
