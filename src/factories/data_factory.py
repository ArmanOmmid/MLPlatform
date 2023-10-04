
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

    if config.dataset in STANDARD_DATASETS:
        return standard.get_standard_dataset(config, download=True)
    else:
        return getattr(custom, config.dataset)(config)
