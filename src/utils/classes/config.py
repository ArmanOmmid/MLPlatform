
from typing import Union
import yaml
import os

class Config(dict):

    @classmethod
    def _set_metadata(cls, configs_compile_path: str, extension: str, dirname_field: str, filename_field: str, encounter_limit: int):
        """
        Sets up metadata to help the Config instantiation

        Args:
            configs_compile_path (str): path to the configs folder 
            extension (str): choice of .yaml or .yml
            dirname_field (str): for config yaml file pointers, define the field for the dirname
            filename_field (str): for config yaml file pointers, define the field for the filename
            ecnounter_limit (int): helps perevent config pointer loops
        """
        cls._metadata = {
            "compile_path" : configs_compile_path,
            "encounters" : {}
        }
        cls.extension = extension
        cls.dirname_field = dirname_field
        cls.filename_field = filename_field
        cls.encounter_limit = encounter_limit

    @staticmethod
    def read_yaml(yaml_path: str, prior: dict=None) -> dict:
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

    def __init__(self, config_dict):
        """
        Setup Configs then call to dictionary superconstructor and assigned self.__dict__ to self
        """
        self._setup(config_dict)
        super().__init__(config_dict)
        self.__dict__ = self

    def _setup(self, config: Union[dict, list]) -> None:
        """
        Recursively builds Configs and sets config pointers in-place
        """
        if isinstance(config, dict):
            for key in config.keys():
                value = config[key]
                # Its a file pointer if its a dictionary key, value where the value is a string starting with "$"
                if isinstance(config[key], str) and value[0] == "$":
                    config[key] = self._handle_pointer(key, value)

                if isinstance(config[key], dict):
                    config[key] = Config(config[key])
                elif isinstance(config[key], list):
                    self._setup(config[key])

        elif isinstance(config, list):
            for i in range(len(config)):
                if isinstance(config[i], dict):
                    config[i] = Config(config[i])
                elif isinstance(config[i], list):
                    self._setup(config[i])

    def _handle_pointer(self, key: str, value: str) -> dict:
        """
        Handle config file pointer
        """

        # Prevent subconfig loops by raising an error if a subconfig is encountered too many times
        if (key, value) not in self._metadata["encounters"]:
            self._metadata["encounters"][(key, value)] = 0
        elif self._metadata["encounters"][(key, value)] > self.encounter_limit:
            raise KeyError(f"Subconfig Encounter Limit Reached ({self.encounter_limit}), Potential Cycle for {{ {key} : {value} }}")
        
        # Read the file pointed to and return the subconfig
        subconfig = self.read_yaml(
            os.path.join(self._metadata["compile_path"], key, value[1:] + self.extension), 
            prior = {self.dirname_field : key,
                     self.filename_field : value[1:]})
        # Do any postprocessing on the metadata
        self._metadata["encounters"][(key, value)] += 1

        return subconfig
    
    def __getattr__(self, field):
        if field not in self:
            # REMOVED FOR NOW: If its from a config pointer (check by seeing if _name exists), provide the dirname and filename too
            pointer_id = "" # f"{self[self.dirname_field]}:{self[self.filename_field]}." if self.get(self.filename_field, False) else ""
            print(f"Config Undefined Key Warning: '{pointer_id}{field}' - Returning None")
            return None
        return self.__dict__[field]

    
    def save(self, save_path: str=None):
        """
        Save Config to a save path. If save path is None, use config.path.config
        """
        if save_path: save_path = self.config_path
        with open(save_path, "w") as yaml_file:
            yaml.dump(self.primitive(), yaml_file, default_flow_style=False)

    def primitive(self, element="__None__"):
        """
        Serialize / Primitivize the Config object
        """
        if element == "__None__": element = self
        if isinstance(element, (Config, dict)):
            serialized = {}
            for key, value in element.items():
                serialized[key] = self.primitive(value)
        elif isinstance(element, list):
            serialized = []
            for value in element:
                serialized.append(self.primitive(value))
        else:
            serialized = element
        return serialized
