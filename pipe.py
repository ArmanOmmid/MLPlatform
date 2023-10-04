
import os
import sys
from subprocess import Popen, PIPE, STDOUT

from argparser import build_argparser
from src.utils import get_locations, make_locations

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SUB_PROGRAM = "main.py"

def main(args, inherited_args):

    enable_output = not args.disable_output
    if enable_output:
        locations = get_locations(args.working_directory)
        output_path = os.path.join(locations["outputs"], args.experiment_name)
        terminal_path = os.path.join(output_path, "terminal.txt")

    main_program = os.path.join(PROJECT_ROOT, SUB_PROGRAM)
    command = ['python3', main_program] + inherited_args + sys.argv[1:]

    command_string = " ".join(command) + "\n\n"
    sys.stdout.write(command_string)

    if enable_output: make_locations(output_path)
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    
    # Open Terminal File
    if enable_output:
        terminal_file = open(terminal_path, "wb")
        terminal_file.write(command_string.encode("utf-8"))

    # Write STDOUT
    for line in iter(process.stdout.readline, b""):
        if enable_output: terminal_file.write(line)
        sys.stdout.write(line.decode())

    # Write STDERR
    for line in iter(process.stderr.readline, b""):
        if enable_output: terminal_file.write(line)
        sys.stderr.write(line.decode())

    exit_code = process.wait()

    # Close Terminal File
    if enable_output: terminal_file.close()

    return exit_code

if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()
    inherited_args = parser.inherit_args(args, sys.argv[1:], parser)
    main(args, inherited_args)
