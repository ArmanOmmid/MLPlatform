
from src.arch import models

def model_factory(config):

    model = models.UNet()
    model.load(weights_path=config.weights, map_location=config.device)
    model.to(config.device)
    
    return model
