
import time
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as T 
import torchinfo

from src.factories import data_factory, model_factory
from src.data.utils import split_dataset
from src.experiments.modules import run_training

def standard_experiment(config):

    dataset = data_factory(config)
    dataset.set_transforms()

    # May need class count for model. Infer from dataset
    # May need input size for model. This can either be infered from the dataset or can also reshape into a custom resolution

    model = model_factory(config)

    dataset_len = len(dataset)
    input_shape, targets_shape = dataset[0][0].shape, dataset[0][1].shape

    # Setup other objects

    criterion = torch.nn.BCEWithLogitsLoss() # We can also define these within each model or dataset!
    accuracy_metric = None # We can also define these within each model or dataset!

    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, config.epochs)

    if config.torchinfo:
        summary_columns =[ "input_size", "output_size", "num_params", "params_percent", "kernel_size", "mult_adds", "trainable"]
        summary = torchinfo.summary(model=model, input_size=(config.batch_size, *input_shape), col_names=summary_columns)
        config.output("torchinfo.txt", summary)

    train, val = split_dataset(dataset, config.val) # Returns None for val if we are not doing validation

    train_loader = DataLoader(train, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=True)
    val_loader = DataLoader(val, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=False) if val else None

    # Run epochs

    results = run_training(
        config,
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        scheduler,
        accuracy_metric
    )

    return results
