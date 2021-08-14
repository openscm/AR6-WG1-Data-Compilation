from pathlib import Path

import pytest
import scmdata.testing

from openscm_ar6_wg1_data_compilation import (
    compile_spm_fig_1_timeseries
)


def test_spm_fig_1_timeseries_generation(raw_data_dir, processed_data_dir):
    fig_spm1_data_dir = str(Path(raw_data_dir) / "dap.ceda.ac.uk" / "badc" / "ar6_wg1" / "data" / "spm" / "spm_01" / "v20210809")
    target_file = str(Path(processed_data_dir) / "fig-spm1-timeseries" / "fig-spm1-timeseries.csv")

    res = compile_spm_fig_1_timeseries(fig_spm1_data_dir)

    exp = scmdata.ScmRun(target_file)

    scmdata.testing.assert_scmdf_almost_equal(res, exp)
