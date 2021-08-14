"""
Processing of data from SPM Fig. 1

Notes from compiling:

- gmst_changes_model_and_obs.csv has a typo, "ensamble" should be "ensemble"
- are panel b obs really HadCRUT4, look more like HadCRUT5?
- the CMIP6 simulations stop before obs in the figure so why do they both have data here
"""
from pathlib import Path

import pandas as pd
import scmdata

from .badc import read_badc
from .utils import convert_percentile_to_stats, convert_ssp_name, force_col_to_int


def compile_spm_fig_8_timeseries(raw_data_path):
    directories_metadata = (
        # path, start_string, metadata
        (
            Path("panel_a"),
            "tas_global_",
            dict(
                variable="Surface Air Temperature Change",
                unit="K",
                region="World",
                reference_period_start_year=1850,
                reference_period_end_year=1900,
                model="Ch.4 Assessed",
            ),
        ),
        (
            Path("panel_b"),
            "sia_arctic_september_",
            dict(
                variable="Arctic Sea Icea Area|September",
                unit="Mm^2",
                region="World",
                model="CMIP6 multi-model ensemble",
            ),
        ),
        (
            Path("panel_c"),
            "phos_global_",
            dict(
                variable="Ocean Surface pH",
                unit="dimensionless",
                region="World",
                model="CMIP6 multi-model ensemble",
            ),
        ),
    )

    out = []
    for directory, start_string, metadata in directories_metadata:
        for filename in (raw_data_path / directory).glob("*.csv"):
            stem = Path(filename).stem
            assert stem.startswith(start_string)
            scenario = stem.split(start_string)[-1].replace("_", "").lower()

            raw = pd.read_csv(filename).set_index("Year")
            raw.columns.name = "percentile"
            stacked = raw.stack().reset_index().rename({0: "value"}, axis="columns")
            stacked.columns = stacked.columns.str.lower()

            stacked["scenario"] = convert_ssp_name(scenario)
            for k, v in metadata.items():
                stacked[k] = v

            out.append(scmdata.ScmRun(stacked))

    out = scmdata.run_append(out)
    out["variable"] = out["variable"] + "|" + out["percentile"]

    # hack to force int
    for c in ["reference_period_start_year", "reference_period_end_year"]:
        out = force_col_to_int(out, c)

    out = out.drop_meta("percentile")
    return out
