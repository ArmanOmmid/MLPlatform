
import torch
from src.utils import set_seed

from src.factories import data_factory, model_factory

def execution(config):

    set_seed(config.seed)

    config.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    train, val, test = data_factory(config)

    model = model_factory(config)
    
    