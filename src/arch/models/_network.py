
from abc import ABC

import os

import torch
import torch.nn as nn

WEIGHTS_EXTENSION = ".pth"

class _Network(nn.Module, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self, weights_path: str=None, map_location: str="cpu"):
        """
        Load weights if weights were specified
        """
        if not weights_path: return
        self.load_state_dict(torch.load(weights_path, map_location=torch.device(map_location)))

    def save(self, path: str, tag: str, filename: str="weights.pth"):
        """
        All saves should be under the same path folder, under different tag folders, with the same filename
        """
        filename = filename.split(".")[0] + WEIGHTS_EXTENSION
        save_path = os.path.join(path, tag, filename)
        torch.save(self.state_dict(), save_path)
