"""
Processing of data from SPM Fig. 10
"""
from pathlib import Path

import pandas as pd
import scmdata

from .utils import convert_ssp_name, force_col_to_int


def compile_spm_fig_10_timeseries(raw_data_path):
    complete_output = []

    region = "World"
    common_metadata = {"region": region}

    for filename in Path(raw_data_path).glob("Top_panel*.csv"):
        scenario = filename.stem.replace("Top_panel_", "").lower().replace("-", "")

        raw = pd.read_csv(filename, header=None)
        if scenario == "history":
            raw.columns = ["variable", "unit"] + list(range(1850, 2019 + 1))
            cumulative_co2_model = "Friedlingstein et al. (2020)"
            gsat_model = "Ch.2 assessment"
        else:
            raw.columns = ["variable", "unit"] + list(range(2015, 2050 + 1))
            cumulative_co2_model = "IAMs"
            gsat_model = "Ch.4 assessment"

        raw["unit"] = raw["unit"].str.replace("°C", "K")

        def extract_percentile(v):
            if v.startswith("Cumulative CO2 emissions"):
                return ""

            if v == "Assessed global surface temperature relative to 1850-1900 (Ch2)":
                return "Mean"

            percentile = v.split("- ")[-1].split("(")[-1].strip(")")
            if percentile.startswith("central"):
                return "Mean"
            if percentile.startswith("5th percentile"):
                return "5%"
            if percentile.startswith("95th percentile"):
                return "95%"

            raise NotImplementedError(v)

        raw["percentile"] = raw["variable"].apply(extract_percentile)

        def extract_reference_period(v):
            if v.startswith("Cumulative CO2 emissions since 1850"):
                return "1850-1850"
            if "relative to 1850-1900" in v:
                return "1850-1900"
            if v.startswith("Human-caused"):
                # stated in data README
                return "1850-1900"

            raise NotImplementedError(v)

        raw["reference_period"] = raw["variable"].apply(extract_reference_period)
        raw["reference_period_start_year"] = raw["reference_period"].apply(
            lambda x: x.split("-")[0]
        )
        raw["reference_period_end_year"] = raw["reference_period"].apply(
            lambda x: x.split("-")[-1]
        )

        def rename_variable(v):
            if v.startswith("Cumulative CO2 emissions"):
                return "Cumulative Emissions|CO2"

            if v.startswith("Assessed GSAT"):
                return "Surface Air Temperature Change"

            if v == "Assessed global surface temperature relative to 1850-1900 (Ch2)":
                return "Surface Air Temperature Change"

            if v.startswith("Human-caused warming"):
                return "Surface Air Temperature Change|Anthropogenic"

            raise NotImplementedError(v)

        raw["variable"] = raw["variable"].apply(rename_variable)

        model_map = {
            "Surface Air Temperature Change": gsat_model,
            "Surface Air Temperature Change|Anthropogenic": gsat_model,
            "Cumulative Emissions|CO2": cumulative_co2_model,
        }
        raw["model"] = raw["variable"].map(model_map)
        raw["scenario"] = scenario.replace("history", "historical")

        for k, v in common_metadata.items():
            raw[k] = v

        out = scmdata.ScmRun(raw)
        complete_output.append(out)

    complete_output = scmdata.run_append(complete_output)
    complete_output["scenario"] = complete_output["scenario"].apply(convert_ssp_name)
    complete_output["variable"] = complete_output["variable"] + complete_output[
        "percentile"
    ].apply(lambda x: "|{}".format(x) if x else x)
    complete_output = complete_output.drop_meta(["percentile", "reference_period"])

    return complete_output
