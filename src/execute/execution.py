
from src.utils import set_seed
from src.data.datasets import get_dataset, split_dataset

def execution(config):

    set_seed(config.seed)

    train, test = get_dataset(config.dataset, config.path.downloads, download=True)
    train, val = split_dataset(train, 0.2)


    