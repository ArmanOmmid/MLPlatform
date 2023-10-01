
import os
import torch
import torchvision
from torch.utils.data import random_split

def get_dataset(dataset_name: str, data_folder_path: str, download: bool = False):
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
    train_dataset = getattr(torchvision.datasets, dataset_name)(os.path.join(data_folder_path, dataset_name, "train"), download=download, train=True)
    test_dataset = getattr(torchvision.datasets, dataset_name)(os.path.join(data_folder_path, dataset_name, "test"), download=download, train=False)
    return train_dataset, test_dataset

def split_dataset(dataset: torchvision.datasets, split_percent: float):
    """
    Splits the dataset

    Args:
        dataset (torch.vision.datasets): pytorch dataset object
        split_percent (float): percentage of dataset to split into
    
    Returns:
        subset_1 (torch.vision.datasets.Subset): (1.0 - split_percent) % of the data
        subset_2 (torch.vision.datasets.Subset): (split_percent) % of the data
    """
    total_count = len(dataset)
    count_1 = int(split_percent * (1.0 - total_count))
    count_2 = total_count - count_1
    subset_1, subset_2 = random_split(dataset, [count_1, count_2])
    return subset_1, subset_2
