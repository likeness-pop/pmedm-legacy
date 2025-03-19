import re

import numpy
import pandas
import pytest

import pmedm_legacy

################################################################################
# DEPRECATED -- REMOVE PRIOR TO v0.1.0 RELEASE -- SEE GL:pmedm_legacy#53


def test_quick_validate(pup_0100100, pmd_0100100):
    with pytest.warns(
        FutureWarning,
        match=re.escape(
            "``quick_validate()`` is being deprecated in favor of ``moe_fit_rate()``, "
            "and will be removed prior to ``v0.1.0``. Update code accoringly."
        ),
    ):
        observed = pmedm_legacy.diagnostics.quick_validate(pup_0100100, pmd_0100100)

    assert isinstance(observed, dict)
    assert len(observed) == 2

    observed_ycomp = observed["Ycomp"]
    assert isinstance(observed_ycomp, pandas.DataFrame)
    assert observed_ycomp.shape == (9165, 6)
    pandas.testing.assert_index_equal(
        observed_ycomp.columns,
        pandas.Index(["constraint", "acs", "pmedm", "err", "moe", "in_moe"]),
    )
    assert (observed_ycomp.index.str.startswith(pytest.data_0100100["st_fips"])).all()

    observed_moe_fit_rate = observed["moe_fit_rate"]
    assert isinstance(observed_moe_fit_rate, numpy.float64)
    assert observed_moe_fit_rate > 0.99


################################################################################


def test_moe_fit_rate(pup_0100100, pmd_0100100):
    observed = pmedm_legacy.diagnostics.moe_fit_rate(
        pup_0100100.est_ind,
        pup_0100100.est_g2,
        pup_0100100.se_g2,
        pmd_0100100.pmedm_res["almat"],
    )

    assert isinstance(observed, dict)
    assert len(observed) == 2

    observed_ycomp = observed["Ycomp"]
    assert isinstance(observed_ycomp, pandas.DataFrame)
    assert observed_ycomp.shape == (9165, 6)
    pandas.testing.assert_index_equal(
        observed_ycomp.columns,
        pandas.Index(["constraint", "acs", "pmedm", "err", "moe", "in_moe"]),
    )
    assert (observed_ycomp.index.str.startswith(pytest.data_0100100["st_fips"])).all()

    observed_moe_fit_rate = observed["moe_fit_rate"]
    assert isinstance(observed_moe_fit_rate, numpy.float64)
    assert observed_moe_fit_rate > 0.99
