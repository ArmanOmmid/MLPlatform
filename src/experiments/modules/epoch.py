
from typing import Callable
import torch
from torch.nn import Module
from torch.utils.data import DataLoader
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer

def run_epoch(
        config,
        model: Module,
        data_loader: DataLoader,
        criterion: _Loss,
        optimizer: Optimizer,
        accuracy_metric: Callable = None,
        learn = True
    ):

    dataset_len = len(data_loader.dataset)
    epoch_loss = 0
    epoch_accuracy = 0 if accuracy_metric else None
    
    for iter, (input, target) in enumerate(data_loader):
        input, target = input.to(config.device), target.to(config.device)

        model.train(learn)
        if learn: 
            optimizer.zero_grad()

        with torch.set_grad_enabled(learn):

            output = model(input)
            loss = criterion(output, target)

            if learn:
                loss.backward()
                optimizer.step()

        model.train(False)

        epoch_loss += loss.item() * input.size(0)
        if accuracy_metric:
            epoch_accuracy += accuracy_metric(output, target) 

    avg_epoch_loss = epoch_loss / dataset_len
    avg_epoch_accuracy = epoch_accuracy / dataset_len if accuracy_metric else None
    return avg_epoch_loss, avg_epoch_accuracy
