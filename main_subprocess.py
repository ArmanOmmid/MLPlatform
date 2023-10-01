
import os

from argparser import build_argparser

from src.utils import set_seed, build_config, make_locations, save_config
from src.execute import execution

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIGS_PATH = os.path.join(PROJECT_ROOT, "configs")

def main(args, unkown_args):

    config = build_config(
                configs_path=CONFIGS_PATH,
                working_directory=args.working_directory, 
                experiment_name=args.experiment_name)
    make_locations(config.downloads, config.output)
    save_config(config)
    set_seed(config.seed)

    execution(config)

if __name__ == "__main__":
    parser = build_argparser()
    args, unkown_args = parser.parse_known_args()
    main(args, unkown_args)
