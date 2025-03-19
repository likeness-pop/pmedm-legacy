import contextlib
from importlib.metadata import PackageNotFoundError, version

from .diagnostics import moe_fit_rate, quick_validate
from .parallel import make_solve, parallel_solve
from .pmedm import PMEDM

with contextlib.suppress(PackageNotFoundError):
    __version__ = version("pmedm_legacy")
