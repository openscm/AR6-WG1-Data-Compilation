"""
Processing of data from SPM Fig. 4
"""
from pathlib import Path

import pandas as pd
import scmdata

from .utils import convert_ssp_name


def compile_spm_fig_4_timeseries(raw_data_path):
    complete_output = []

    region = "World"
    common_metadata = {"region": region}

    basic_csv_files = (
        # path, metadata
        (
            Path("panel_a") / "Carbon_dioxide_Gt_CO2_yr.csv",
            {
                "model": "IAMs",
                "variable": "Emissions|CO2",
                "unit": "GtCO2 / yr",
                **common_metadata,
            },
        ),
        (
            Path("panel_a") / "Nitrous_oxide_Mt_N2O_yr.csv",
            {
                "model": "IAMs",
                "variable": "Emissions|N2O",
                "unit": "MtN2O / yr",
                **common_metadata,
            },
        ),
        (
            Path("panel_a") / "Methane_Mt_CO2_yr.csv",
            {
                "model": "IAMs",
                "variable": "Emissions|CH4",
                "unit": "MtCH4 / yr",
                **common_metadata,
            },
        ),
        (
            Path("panel_a") / "Sulfur_dioxide_Mt_SO2_yr.csv",
            {
                "model": "IAMs",
                "variable": "Emissions|Sulfur",
                "unit": "MtSO2 / yr",
                **common_metadata,
            },
        ),
    )

    for filepath, metadata in basic_csv_files:
        raw = pd.read_csv(Path(raw_data_path) / filepath)

        raw_renamed_cols = (
            raw.rename({"years": "year"}, axis="columns").set_index("year").sort_index()
        )
        raw_renamed_cols.columns.name = "scenario"
        stacked = (
            raw_renamed_cols.stack().reset_index().rename({0: "value"}, axis="columns")
        )

        for c, v in metadata.items():
            stacked[c] = v

        out = scmdata.ScmRun(stacked)
        complete_output.append(out)

    complete_output = scmdata.run_append(complete_output)
    complete_output["scenario"] = complete_output["scenario"].apply(convert_ssp_name)

    return complete_output
