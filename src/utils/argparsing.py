import argparse

class InheritAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values if values is not None else self.default)

def inherit_args(args: argparse.Namespace, argv: list, parser: argparse.ArgumentParser):
    """
    We want to directly pass in sys.argv[1:]
    But we want to pass in some default values defined in main.py and not let them be redefined in main_program.py
    """

    # Get arguments that are are InheritActions that we designate to pass down their default values
    carryover_flags = []
    for action in parser._actions:
        if isinstance(action, InheritAction):
            carryover_flags.append(action.option_strings)
    
    # Iterate through their associated flags and if sys.argv does not have them, pass them on into carryover_args
    carryover_args = []
    for flags in carryover_flags:
        short_flag = flags[0]
        long_flag = flags[1]
        if short_flag not in argv and long_flag not in argv:
            carryover_args.append(long_flag)
            carryover_args.append(getattr(args, long_flag[2:]))
    return carryover_args

def recover_arguments(args: argparse.Namespace):
    """
    Recovers arguments from an argparse.Namespace objects
    """
    args_list = []
    for arg_name, arg_value in vars(args).items():
        if arg_value is not None:
            args_list.extend(["--" + arg_name, str(arg_value)])
    return args_list
