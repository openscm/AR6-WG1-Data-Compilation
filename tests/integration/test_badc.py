import numpy.testing as npt
import pandas as pd

from openscm_ar6_wg1_data_compilation import read_badc

EXP_SIMPLE_DATA = pd.DataFrame(
    [
        [0.8, 2.4, 2.3],
        [1.1, 3.4, 3.3],
        [2.4, 3.5, 3.3],
        [3.7, 6.7, 6.4],
        [4.9, 5.7, 5.8],
    ],
    columns=["time", "air temperature", "met station air temperature"],
)


def test_parse_simple_file(test_data_dir):
    """Test parsing an example file from https://help.ceda.ac.uk/article/105-badc-csv"""
    obs, obs_units, obs_meta = read_badc(test_data_dir / "simple-badc-example.csv")
    pd.testing.assert_frame_equal(obs, EXP_SIMPLE_DATA)

    assert obs_units == {
        "time": "days since 2007-03-14",
        "air temperature": "unspecified",
        "met station air temperature": "unspecified",
    }
    assert obs_meta == {
        "met station air temperature": {"creator": "unknown,Met Office"},
        "time": {"coordinate_variable": "x"},
    }


def test_parse_spm_fig1_panel_b(test_data_dir):
    obs, obs_units, obs_meta = read_badc(test_data_dir / "spm-fig1-panelb.csv")

    assert obs.shape == (170, 8)
    assert obs.columns.tolist() == [
        "Year",
        "gsta_brown_line_hist_ssp245",
        "gsta_brown_shading_bottom_hist_ssp245",
        "gsta_brown_shading_top_hist_ssp245",
        "gsta_green_line_hist_nat",
        "gsta_green_shading_bottom_hist_nat",
        "gsta_green_shading_top_hist_nat",
        "gsta_black_obs",
    ]
    npt.assert_allclose(
        obs.loc[obs["Year"] == 1850, "gsta_brown_line_hist_ssp245"], -0.047589067
    )
    npt.assert_allclose(obs.loc[obs["Year"] == 2019, "gsta_black_obs"], 1.226)
    npt.assert_allclose(
        obs.loc[obs["Year"] == 1852, "gsta_brown_shading_top_hist_ssp245"], 0.198392534
    )

    assert obs_units == {
        "Year": "Year",
        "gsta_black_obs": "Degrees C",
        "gsta_brown_line_hist_ssp245": "Degrees C",
        "gsta_brown_shading_bottom_hist_ssp245": "Degrees C",
        "gsta_brown_shading_top_hist_ssp245": "Degrees C",
        "gsta_green_line_hist_nat": "Degrees C",
        "gsta_green_shading_bottom_hist_nat": "Degrees C",
        "gsta_green_shading_top_hist_nat": "Degrees C",
    }

    assert obs_meta["Year"]["coordinate_variable"] == "Year,Year"
    assert obs_meta["gsta_brown_line_hist_ssp245"]["comments"] == (
        "Global Surface Temperature Anomalies (GSTA) relative to 1850-1900 from "
        "CMIP6 simulations with human and natural forcing (mean over ensamble),"
    )
    for k, v in obs_meta.items():
        if k == "Year":
            assert list(v.keys()) == ["coordinate_variable", "type"]
        else:
            assert list(v.keys()) == ["comments", "type"]
