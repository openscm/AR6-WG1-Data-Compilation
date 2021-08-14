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
from .utils import convert_percentile_to_stats, force_col_to_int


def compile_spm_fig_1_timeseries(raw_data_path):
    complete_output = []

    unit = "K"
    region = "World"
    reference_period_start_year = 1850
    reference_period_end_year = 1900

    common_metadata = {
        "variable": "Surface Air Temperature Change",
        "unit": unit,
        "region": region,
        "reference_period_start_year": reference_period_start_year,
        "reference_period_end_year": reference_period_end_year,
    }
    basic_csv_files = (
        # path, metadata, column-percentile mapping
        (
            Path("panel_a") / "SPM1_1850-2020_obs.csv",
            {
                "model": "direct observations",
                "scenario": "historical",
                **common_metadata
            },
            {"temp": 0.5}
        ),
        (
            Path("panel_a") / "SPM1_1-2000.csv",
            {
                "model": "paleoclimate archives",
                "scenario": "historical",
                **common_metadata
            },
            {"temp": 0.5, "5%": 0.05, "95%": 0.95}
        ),
    )

    for filepath, metadata, column_percentile_mapping in basic_csv_files:
        raw = pd.read_csv(Path(raw_data_path) / filepath)
        raw_renamed_cols = raw.set_index("year").rename(column_percentile_mapping, axis="columns").sort_index()
        raw_renamed_cols.columns.name = "percentile"
        stacked = raw_renamed_cols.stack().reset_index().rename({0: "value"}, axis="columns")

        for c, v in metadata.items():
            stacked[c] = v

        out = scmdata.ScmRun(stacked)
        complete_output.append(out)

    panel_b_file = Path(raw_data_path) / "panel_b" / "gmst_changes_model_and_obs.csv"
    # TODO: move this into test case of read_badcsv
    panel_b_df, panel_b_units, panel_b_metadata = read_badc(panel_b_file)
    panel_b_df = panel_b_df.set_index("Year")
    panel_b_df.columns.name = "variable"
    panel_b_df = panel_b_df.stack().reset_index().rename({0: "value"}, axis="columns")


    def extract_scenario(v):
        scenario = "hist{}".format(v.split("hist")[-1]).replace("_", "-")

        if scenario == "histgsta-black-obs":
            return "historical"

        return scenario


    panel_b_df["scenario"] = panel_b_df["variable"].apply(extract_scenario)


    def extract_model(v):
        relevant_metadata = panel_b_metadata[v]
        comments = relevant_metadata["comments"]
        if "CMIP6" in comments:
            return "CMIP6 multi-model ensemble"
        if "HadCRUT4.6" in comments:
            return "HadCRUT4.6"

        raise NotImplementedError(v)


    panel_b_df["model"] = panel_b_df["variable"].apply(extract_model)


    def extract_percentile(v):
        relevant_metadata = panel_b_metadata[v]
        comments = relevant_metadata["comments"]
        if "mean over" in comments:
            out = "Mean"
        elif "95%" in comments:
            out = 0.95
        elif "5%" in comments:
            out = 0.05
        elif "observations" in comments:
            # assume best-estimate i.e. median
            out = 0.5
        else:
            raise NotImplementedError(v)

        return out


    panel_b_df["percentile"] = panel_b_df["variable"].apply(extract_percentile)

    panel_b_df["unit"] = panel_b_df["variable"].map(panel_b_units)
    assert (panel_b_df["unit"] == "Degrees C").all()
    assert all([
        f"relative to {reference_period_start_year}-{reference_period_end_year}"
        in v["comments"] for v in panel_b_metadata.values()
    ])
    panel_b_df["unit"] = panel_b_df["unit"].str.replace("Degrees C", unit)

    for c, v in common_metadata.items():
            panel_b_df[c] = v

    panel_b_df.columns = panel_b_df.columns.str.lower()
    complete_output.append(scmdata.ScmRun(panel_b_df))

    complete_output = scmdata.run_append(complete_output)
    complete_output["variable"] = complete_output["variable"] + "|" + complete_output["percentile"].apply(convert_percentile_to_stats, int_percentages=True)
    complete_output = complete_output.drop_meta("percentile")

    for c in ["reference_period_start_year", "reference_period_end_year"]:
        complete_output = force_col_to_int(complete_output, c)

    return complete_output
