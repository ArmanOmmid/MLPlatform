import random
import numpy as np
import torch
from torch.backends import cudnn

def set_seed(seed: int = 0):
    """
    Sets seeds for all libraries
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        cudnn.deterministic = True
        cudnn.benchmark = False
