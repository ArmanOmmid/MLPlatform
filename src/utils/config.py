
from typing import Union
import yaml
import os

from src.utils.locations import get_locations

EXTENSION = ".yaml"
# Encounter limit helps prevent config loops
ENCOUNTER_LIMIT = 1

class Config(dict):
    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.__dict__ = config_dict

def build_config(configs_path: str, working_directory: str, experiment_name: str) -> Config:
    """
    Builds the config object by compiling yaml configs and any other needed items
    """

    config = compile_yaml(configs_path)
    artifact_locations = get_locations(working_directory)

    locations = {
        "downloads" : artifact_locations["downloads"],
        "output" : os.path.join(artifact_locations["outputs"], experiment_name),
        "experiment_name" : experiment_name,
        "working_directory" : working_directory
    }

    config.update(locations)

    config = Config(config)

    return config

def save_config(config: Config):
    save_path = os.path.join(config.output, "config.yaml") 
    with open(save_path, "w") as yaml_file:
        yaml.dump(config.__dict__, yaml_file, default_flow_style=False)

def compile_yaml(configs_path: str) -> dict:
    """
    Compiles config from the main config yaml file with any subconfig yaml file pointers
    """

    configs_metadata = {
        "path" : configs_path,
        "encounters" : {}
    }

    config = read_yaml(os.path.join(configs_path, "config" + EXTENSION))

    setup_pointers(config, configs_metadata)

    return config

def read_yaml(yaml_path: str, prior: dict = None) -> dict:
    """
    Read YAML file given a path. Prior lets you add the new yaml dict to a prior dict
    """
    with open(yaml_path, "r") as yaml_file:
        yaml_dict = yaml.safe_load(yaml_file)
    if prior:
        if not isinstance(prior, dict): raise ValueError("prior argument must be a dict")
        prior.update(yaml_dict)
        yaml_dict = prior
    return yaml_dict

def setup_pointers(config: Union[dict, list], configs_metadata: dict) -> None:
    """
    Sets config pointers for configs and does so in-place
    """
    if isinstance(config, dict):
        for key in config.keys():
            value = config[key]
            # Its a file pointer if its a dictionary key, value where the value is a string starting with "$"
            if isinstance(config[key], str) and value[0] == "$":
                config[key] = handle_pointer(key, value, configs_metadata)
            setup_pointers(config[key], configs_metadata)

    elif isinstance(config, list):
        for i in range(len(config)):
            setup_pointers(config[i], configs_metadata)

def handle_pointer(key: str, value: str, configs_metadata: dict) -> dict:
    """
    Handle config file pointer
    """

    # Prevent subconfig loops by raising an error if a subconfig is encountered too many times
    if (key, value) not in configs_metadata["encounters"]:
        configs_metadata["encounters"][(key, value)] = 0
    elif configs_metadata["encounters"][(key, value)] > ENCOUNTER_LIMIT:
        raise KeyError(f"Subconfig Encounter Limit Reached ({ENCOUNTER_LIMIT}), Potential Cycle for {{ {key} : {value} }}")
    
    # Read the file pointed to and return the subconfig
    subconfig = read_yaml(
        os.path.join(configs_metadata["path"], key, value[1:] + EXTENSION),
        prior = {"__file__" : value[1:]}
    )
    # Do any postprocessing on the metadata
    configs_metadata["encounters"][(key, value)] += 1

    return subconfig
