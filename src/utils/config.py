
import os

import argparse
from src.utils.classes import Config
from src.utils import get_locations

CONFIG_EXTENSION = ".yaml"
DIRNAME_FIELD = "_dname"
FILENAME_FIELD = "_fname"
ENCOUNTER_LIMIT = 1

def build_config(configs_compile_path: str, args: argparse.Namespace) -> Config:
    """
    Builds the config object by compiling yaml configs and any other needed items
    """

    # Read original config
    config = Config.read_yaml(os.path.join(configs_compile_path, "config" + CONFIG_EXTENSION))

    # Setup any additional config variables
    artifact_locations = get_locations(args.working_directory)
    data_path = artifact_locations["data"]
    output_path = os.path.join(artifact_locations["outputs"], args.experiment_name)

    config_path = os.path.join(output_path, "config" + CONFIG_EXTENSION)
    weights_path = os.path.join(output_path, "weights")

    additional_data = {
        "enable_output": not args.disable_output,
        "config_path" : config_path,
        "path" : {
            "data" : data_path,
            "output" : output_path,
            "weights" : weights_path
        },
        "id" : {
            "name" : args.experiment_name,
            "workdir" : args.working_directory
        }
    }

    # Update the config
    config.update(additional_data)

    # Setup Config Metadata and Instatiate the Config object
    Config._set_metadata(configs_compile_path, CONFIG_EXTENSION, DIRNAME_FIELD, FILENAME_FIELD, ENCOUNTER_LIMIT)
    config = Config(config)

    return config
