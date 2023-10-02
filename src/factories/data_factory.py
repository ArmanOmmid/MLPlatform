
from torch.utils.data import DataLoader, Subset
from src.data.datasets import get_dataset, split_dataset

def data_factory(config):
    
    train, test = get_dataset(config.dataset, config.path.downloads, download=True)
    train, val = split_dataset(train, 0.2)

    train_loader = DataLoader(train, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=True)
    val_loader = DataLoader(val, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=False)
    test_loader = DataLoader(test, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=False)

    return train_loader, val_loader, test_loader
