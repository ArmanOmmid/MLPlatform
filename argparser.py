
import os
import datetime
import argparse

TIME_OFFSET = -7
CURRENT_TIME = datetime.datetime.now() + datetime.timedelta(hours=TIME_OFFSET)

EXPERIMENT_NAME = f"experiment_{CURRENT_TIME.strftime('%Y-%m-%d_%H-%M-%S')}"
WORKING_DIRECTORY = os.getcwd()

def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--experiment_name', default=EXPERIMENT_NAME,
                        help="Experiment_Name")
    parser.add_argument('-w', '--working_directory', default=WORKING_DIRECTORY,
                        help="Working Directory")
    return parser

def recover_arguments(args):
    args_list = []
    for arg_name, arg_value in vars(args).items():
        if arg_value is not None:
            args_list.extend(["--" + arg_name, str(arg_value)])
    return args_list
