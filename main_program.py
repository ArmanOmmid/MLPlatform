
import os

from argparser import build_argparser
from src.utils import build_config, make_locations
from src.execute import execution

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIGS_COMPILE_PATH = os.path.join(PROJECT_ROOT, "configs")

def main(args):

    config = build_config(configs_compile_path=CONFIGS_COMPILE_PATH, args=args)

    if config.enable_output:
        make_locations(*list(config.path.values()))
        config.save(config.config_path)

    execution(config)

if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()
    main(args)
