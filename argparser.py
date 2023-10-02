
import os
import datetime
import argparse

from src.utils import InheritAction, inherit_args

TIME_OFFSET = -7
CURRENT_TIME = datetime.datetime.now() + datetime.timedelta(hours=TIME_OFFSET)

EXPERIMENT_NAME = f"experiment_{CURRENT_TIME.strftime('%Y-%m-%d_%H-%M-%S')}"
WORKING_DIRECTORY = os.getcwd()

def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--experiment_name", default=EXPERIMENT_NAME, action=InheritAction,
                        help="Experiment Name")
    parser.add_argument("-w", "--working_directory", default=WORKING_DIRECTORY, action=InheritAction,
                        help="Working Directory")
    parser.add_argument("-x", "--disable_output", action="store_true",
                        help="Disable Output")
    
    # Attach inherit_args function here
    parser.inherit_args = inherit_args
    return parser
