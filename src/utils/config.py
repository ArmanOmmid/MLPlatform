
import os
from src.utils.classes import Config
from src.utils import get_locations

EXTENSION = ".yaml"
FILENAME_FIELD = "_type"
ENCOUNTER_LIMIT = 1

def build_config(configs_path: str, working_directory: str, experiment_name: str) -> Config:
    """
    Builds the config object by compiling yaml configs and any other needed items
    """

    # Get original yaml config
    config = Config.read_yaml(os.path.join(configs_path, "config" + EXTENSION))

    # Setup any additional config variables
    artifact_locations = get_locations(working_directory)
    metadata = {
        "path" : {
            "downloads" : artifact_locations["downloads"],
            "output" : os.path.join(artifact_locations["outputs"], experiment_name),
            "config" : os.path.join(artifact_locations["outputs"], experiment_name, "config" + EXTENSION)
        },
        "id" : {
            "name" : experiment_name,
            "workdir" : working_directory
        }
    }

    # Update the config
    config.update(metadata)

    # Setup Config Metadata and Instatiate the Config object
    Config._set_metadata(configs_path, EXTENSION, FILENAME_FIELD, ENCOUNTER_LIMIT)
    config = Config(config)

    return config
