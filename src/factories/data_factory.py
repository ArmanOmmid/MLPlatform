
from torch.utils.data import Dataset
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

def data_factory(config) -> Dataset:

    if config.dataset in STANDARD_DATASETS:
        dataset = standard.get_standard_dataset(config, download=True)
    else:
        dataset = getattr(custom, config.dataset)(config)

    return dataset
