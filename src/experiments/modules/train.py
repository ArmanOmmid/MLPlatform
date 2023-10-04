
import time
from typing import Callable
from torch.nn import Module
from torch.utils.data import DataLoader
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler

from src.experiments.modules import run_epoch

def run_training(
        config,
        model: Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        criterion: _Loss,
        optimizer: Optimizer,
        scheduler: LRScheduler = None,
        accuracy_metric: Callable = None,
    ):

    enable_validation = (val_loader is not None)

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

        # TODO : Weight saving and early stopping?

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
