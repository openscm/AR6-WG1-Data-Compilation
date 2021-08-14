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


def test_parse_simple_file():
    """Test parsing an example file from https://help.ceda.ac.uk/article/105-badc-csv"""
    obs = read_badc("data/simple-example.csv")
    pd.testing.assert_frame_equal(obs, EXP_SIMPLE_DATA)
