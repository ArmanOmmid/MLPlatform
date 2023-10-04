
import torchvision
from torch.utils.data import random_split

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
