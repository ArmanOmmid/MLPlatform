
import torch

from src.utils import set_seed
from src.execute.experiment import experiment

def execution(config):

    set_seed(config.seed)
    config.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    raise Exception()

    results = experiment(config)

    return results
    
    