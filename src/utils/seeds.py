# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helper functions to help with reproducibility of models. """

import logging
import os
import random
from typing import Optional

import numpy as np
import torch
from torch.backends import cudnn

# from pytorch_lightning.utilities import _TORCH_GREATER_EQUAL_1_7, rank_zero_warn
# from pytorch_lightning.utilities.distributed import rank_zero_only

log = logging.getLogger(__name__)


def set_seed(seed: int = 0):
    """
    Sets seeds for all libraries
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        cudnn.deterministic = True
        cudnn.benchmark = False

# def seed_everything(seed: Optional[int] = None, workers: bool = False) -> int:
#     """
#     Function that sets seed for pseudo-random number generators in:
#     pytorch, numpy, python.random
#     In addition, sets the following environment variables:

#     - `PL_GLOBAL_SEED`: will be passed to spawned subprocesses (e.g. ddp_spawn backend).
#     - `PL_SEED_WORKERS`: (optional) is set to 1 if ``workers=True``.

#     Args:
#         seed: the integer value seed for global random state in Lightning.
#             If `None`, will read seed from `PL_GLOBAL_SEED` env variable
#             or select it randomly.
#         workers: if set to ``True``, will properly configure all dataloaders passed to the
#             Trainer with a ``worker_init_fn``. If the user already provides such a function
#             for their dataloaders, setting this argument will have no influence. See also:
#             :func:`~pytorch_lightning.utilities.seed.pl_worker_init_function`.
#     """
#     max_seed_value = np.iinfo(np.uint32).max
#     min_seed_value = np.iinfo(np.uint32).min

#     try:
#         if seed is None:
#             seed = os.environ.get("PL_GLOBAL_SEED")
#         seed = int(seed)
#     except (TypeError, ValueError):
#         seed = _select_seed_randomly(min_seed_value, max_seed_value)
#         rank_zero_warn(f"No correct seed found, seed set to {seed}")

#     if not (min_seed_value <= seed <= max_seed_value):
#         rank_zero_warn(f"{seed} is not in bounds, numpy accepts from {min_seed_value} to {max_seed_value}")
#         seed = _select_seed_randomly(min_seed_value, max_seed_value)

#     # using `log.info` instead of `rank_zero_info`,
#     # so users can verify the seed is properly set in distributed training.
#     log.info(f"Global seed set to {seed}")
#     os.environ["PL_GLOBAL_SEED"] = str(seed)
#     random.seed(seed)
#     np.random.seed(seed)
#     torch.manual_seed(seed)
#     torch.cuda.manual_seed_all(seed)

#     os.environ["PL_SEED_WORKERS"] = f"{int(workers)}"

#     return seed
