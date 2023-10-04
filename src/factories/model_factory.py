
from src.arch import models

def model_factory(config):

    model_class = getattr(models, config.model)
    model = model_class()
    model.load(weights_path=config.weights, map_location=config.device)
    model.to(config.device)
    
    return model
