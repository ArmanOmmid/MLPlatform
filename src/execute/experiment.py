
import time
import torch
from torch.utils.data import DataLoader
import torchinfo

from src.factories import data_factory, model_factory
from src.data.utils import split_dataset
from src.execute.epoch import run_epoch

def experiment(config):

    dataset = data_factory(config)

    model = model_factory(config)

    # Figure out transforms between dataset and model
    data_transform = CustomTransform(
        lambda x: torch.from_numpy(x),
        lambda x: x.float() / 255,
        lambda x: x.permute(2, 0, 1),
    )
    target_transform = CustomTransform(
        lambda x: torch.from_numpy(x),
        lambda x: x.float() / 255,
    )

    dataset.set_transforms(data_transform, target_transform)
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

    enable_validation = isinstance(config.val, float) and config.val > 0.0
    train, val = split_dataset(dataset, config.val)

    train_loader = DataLoader(train, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=True)
    val_loader = DataLoader(val, batch_size=config.batch_size, num_workers=config.num_workers, shuffle=False) if val else None

    # Run epochs

    train_loss_list = []
    train_accuracy_list = []

    val_loss_list = []
    val_accuracy_list = []

    for epoch in range(config.epochs):

        print("===="*4, f"Epoch {epoch+1} / {config.epochs}", "===="*4)
        time_stamp = time.time()

        train_loss, train_accuracy = run_epoch(config, model, train_loader, criterion, optimizer, accuracy_metric, learn=True)
        train_loss_list.append(train_loss)
        if accuracy_metric: train_accuracy_list.append(train_accuracy)

        if scheduler:
            scheduler.step()

        if enable_validation: # In case we didn't set a validation set
            val_loss, val_accuracy = run_epoch(config, model, val_loader, criterion, optimizer, accuracy_metric, learn=False)

        print(f"Epoch {epoch+1} : Time Elapsed: {(time.time() - time_stamp):6f}")
        print("    Train      | Loss: {}".format(f"{train_loss:.6f}"))
        if enable_validation: print("    Validation | Loss: {}".format(f"{val_loss:.6f}"))

        if enable_validation: 
            val_loss_list.append(val_loss)
            if accuracy_metric: val_accuracy_list.append(val_accuracy)

    results = {
        "train" : {},
        "val" : {}
    }
    results["train"]["loss"] = train_loss_list
    results["train"]["accuracy"] = train_accuracy_list if accuracy_metric else None
    if enable_validation:
        results["val"]["loss"] = val_loss_list
        results["val"]["accuracy"] = val_accuracy_list if accuracy_metric else None

    return results


class CustomTransform:
    def __init__(self, *transforms):
        self.transforms = transforms

    def __call__(self, x):
        for transform in self.transforms:
            x = transform(x)
        return x
