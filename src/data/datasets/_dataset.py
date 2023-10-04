
from abc import ABC, abstractmethod
from torch.utils.data import Dataset
import torchvision.transforms as T

class _Dataset(Dataset, ABC):
    def __init__(self) -> None:
        super().__init__()

        self.input_transform = None
        self.target_transform = None

    def transform(self, input, target):
        if self.input_transform:
            input = self.input_transform(input)
        if self.target_transform:
            target = self.target_transform(target)
        return input, target

    def set_transform(self):
        """
        Implement this in the subclass
        """
        pass

    def add_transforms(self, input_transform=None, target_transform=None):
        """
        If a transform is provided, set it. If transforms already exists, append it with compose
        """
        if input_transform:
            if self.input_transform is None:
                self.input_transform = input_transform
            else:
                self.input_transform = T.Compose([
                    self.input_transform,
                    input_transform
                ])
        if target_transform:
            if self.target_transform is None:
                self.target_transform = target_transform
            else:
                self.target_transform = T.Compose([
                    self.target_transform,
                    target_transform
                ])
