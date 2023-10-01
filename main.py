
import os
import sys
from subprocess import Popen, PIPE, STDOUT

from argparser import build_argparser, recover_arguments
from src.utils import get_locations, make_locations

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SUB_PROGRAM = "main_process.py"

def main(args, unkown_args):

    locations = get_locations(args.working_directory)
    output_path = os.path.join(locations["outputs"], args.experiment_name)
    terminal_path = os.path.join(output_path, "terminal.txt")

    main_program = os.path.join(PROJECT_ROOT, SUB_PROGRAM)
    command = ['python3', main_program] + recover_arguments(args) + unkown_args

    command_string = " ".join(command) + "\n\n"
    sys.stdout.write(command_string)

    make_locations(output_path)
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    
    with open(terminal_path, "wb") as terminal_file:

        terminal_file.write(command_string.encode("utf-8"))

        for line in iter(process.stdout.readline, b""):
            terminal_file.write(line)
            sys.stdout.write(line.decode())

        for line in iter(process.stderr.readline, b""):
            terminal_file.write(line)
            sys.stderr.write(line.decode())

        exit_code = process.wait()

    return exit_code

if __name__ == "__main__":
    parser = build_argparser()
    args, unkown_args = parser.parse_known_args()
    main(args, unkown_args)
