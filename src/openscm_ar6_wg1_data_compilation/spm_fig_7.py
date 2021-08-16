"""
Processing of data from SPM Fig. 7
"""
from pathlib import Path

import pandas as pd
import pyam
import scmdata

from .utils import convert_ssp_name


def compile_spm_fig_7_timeseries(raw_data_path):
    data = pd.read_csv(Path(raw_data_path) / "SPM7_data.csv")[0:3]

    # wrange with the raw data
    data = data.T
    variables = data.loc["Unnamed: 0"].values
    data.columns = variables
    data = data[1:]  # remove first line which has variable names
    data.index.name = "scenario"
    data["year"] = 2100
    data = data.reset_index()
    # unify scenario names with other output
    data["scenario"] = data["scenario"].str.strip().str.lower().apply(convert_ssp_name)

    # cast to an IamDataFrame
    df = pyam.IamDataFrame(data, model="IAMs", region="World", value=variables, unit="PgC")

    # rename the variable
    mapping = dict([(i, "Cumulative Carbon Stored|" + i.split(" ")[0].title()) for i in df.variable])
    df.rename(variable=mapping, inplace=True)

    # Return via scmdata to make later checks work smoothly.
    # We'd have to be careful if there was metadata we wanted to keep here.
    out = scmdata.ScmRun(df.timeseries())

    return out
