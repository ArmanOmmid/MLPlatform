
from typing import List
import os

ARTIFACT_DIRS = [
    "downloads",
    "outputs"
]

def get_locations(working_directory: str):
    """
    Make and get artifact locations

    Args:
        working_directory (str): working_directory to create artifacts directory under

    Returns:
        artifact_locations (Dict[str, str]): dictionary with paths to different artifact locations
    """
    artifact_locations = {}
    artifacts_path = os.path.join(working_directory, "artifacts")
    for dirname in ARTIFACT_DIRS:
        artifact_locations[dirname] = os.path.join(artifacts_path, dirname)
    return artifact_locations

def make_locations(*locations: List[str]):
    for location in locations:
        if not os.path.exists(location): os.makedirs(location)
