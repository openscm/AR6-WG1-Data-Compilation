"""
Functions for compiling AR6 WG1 data
"""
import scmdata

from . import _version
from .badc import read_badc
from .spm_fig_1 import compile_spm_fig_1_timeseries
from .spm_fig_4 import compile_spm_fig_4_timeseries
from .spm_fig_7 import compile_spm_fig_7_timeseries
from .spm_fig_8 import compile_spm_fig_8_timeseries
from .spm_fig_10 import compile_spm_fig_10_timeseries

__version__ = _version.get_versions()["version"]
