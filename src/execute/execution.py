
from src.data.datasets import get_dataset, split_dataset

def execution(config):

    train, test = get_dataset(config.dataset, config.downloads, download=True)
    train, val = split_dataset(train, 0.2)

    