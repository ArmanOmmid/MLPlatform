
import torch

from src.utils import set_seed
from src import experiments

def execution(config):

    set_seed(config.seed)
    config.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    results = getattr(experiments, config.experiment)(config)

    return results
