
from torch.utils.data import DataLoader

from src.data.utils import split_dataset
from src.data.datasets import standard, custom

STANDARD_DATASETS = [
    "CIFAR10",
    "CIFAR100",
    "MNIST",
    "FashionMNIST",
    "StanfordCars"
    "Food101"
]

def data_factory(config):

    dataset = get_dataset(config)

    # If a trainval split was requested, oblige
    if config.mode == "train" and config.val:
        dataset_1, dataset_2 = split_dataset(dataset)
        dataloader_1 = DataLoader(dataset_1, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=True)
        dataloader_2 = DataLoader(dataset_2, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=False)
        return dataloader_1, dataloader_2
    
    else:
        shuffle_condition = config.mode == "train"
        dataloader = DataLoader(dataset, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=shuffle_condition)
        return dataloader
        
def get_dataset(config):
    if config.dataset in STANDARD_DATASETS:
        return standard.get_standard_dataset(config, download=True)
    else:
        return getattr(custom, config.dataset)(config)
