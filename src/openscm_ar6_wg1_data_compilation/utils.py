import numpy as np
import pandas as pd


def convert_percentile_to_stats(q, int_percentages=False):
    if q == "Mean":
        return "Mean"

    if q == 0.5:
        return "Median"

    percent = q * 100
    if int_percentages:
        percent = int(percent)

    return f"{percent}%"


def convert_ssp_name(s):
    mapping = {
        "historical": "historical",
        "ssp119": "SSP1-1.9",
        "ssp126": "SSP1-2.6",
        "ssp245": "SSP2-4.5",
        "ssp370": "SSP3-7.0",
        "ssp434": "SSP4-3.4",
        "ssp460": "SSP4-6.0",
        "ssp585": "SSP5-8.5",
        "ssp534-over": "SSP5-3.4-over",
    }

    return mapping[s]



def _force_to_int_representation(inp):
    if np.isnan(inp):
        return ""

    return str(int(inp))


def force_col_to_int(inp, c):
    out = inp.copy()
    out[c] = out[c].apply(_force_to_int_representation)

    return out
