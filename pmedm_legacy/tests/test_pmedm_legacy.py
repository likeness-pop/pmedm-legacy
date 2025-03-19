import numpy
import pandas
import pytest
import rpy2

import pmedm_legacy

ARRAY_len1 = numpy.array([0])
ARRAY_len2 = numpy.array([0, 0])

SERIES_len1 = pandas.Series(ARRAY_len1)
SERIES_len2 = pandas.Series(ARRAY_len2)

DF_len1 = pandas.DataFrame(SERIES_len1)
DF_len2 = pandas.DataFrame(SERIES_len2)


class TestPMEDM:
    def test_from_super_tract(self, pup_0100100):
        pmd = pmedm_legacy.PMEDM(
            pup_0100100.year,
            pup_0100100.wt,
            pup_0100100.est_ind,
            pup_0100100.est_g2,
            pup_0100100.est_g1,
            pup_0100100.se_g2,
            pup_0100100.se_g1,
            g1=pup_0100100.g1,
            g2=pup_0100100.g2,
            tr_iter=50,
            tr_tol=1e-3,
        )
        pmd.solve()

        observed_almat = pmd.pmedm_res["almat"]
        assert observed_almat.dtype == float
        assert observed_almat.shape == (
            pup_0100100.wt.shape[0],
            pup_0100100.est_g2.shape[0],
        )

        observed_serialno = pmd.pmedm_res["serialno"]
        assert observed_serialno.dtype == "<U13"
        assert observed_serialno.shape == (pup_0100100.wt.shape[0],)

        observed_geoid = pmd.pmedm_res["geoid"]
        assert observed_geoid.dtype == "<U11"
        assert observed_geoid.shape == (pup_0100100.est_g2.shape[0],)

    def test_null_types(self):
        pmd = pmedm_legacy.PMEDM(
            pytest.YEAR, ARRAY_len2, DF_len2, DF_len2, DF_len1, DF_len2, DF_len1
        )

        assert isinstance(pmd, pmedm_legacy.PMEDM)

        attrs = ["g2", "g1", "tr_iter", "tr_tol"]
        for attr in attrs:
            attr_val = getattr(pmd, attr)
            if isinstance(attr_val, rpy2.rinterface.NULLType):
                assert str(attr_val.typeof) == "0"
            else:
                raise RuntimeError("Failsafe -- this will not happen.")


class TestPMEDMInputValidation:
    def test_invalid_year(self):
        with pytest.raises(ValueError, match="``year`` must be an integer."):
            pmedm_legacy.PMEDM(
                "xyz", ARRAY_len2, DF_len2, DF_len2, DF_len1, DF_len2, DF_len1
            )

    def test_invalid_wt(self):
        with pytest.raises(
            ValueError, match="``wt`` and ``est_ind`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len1, DF_len2, DF_len2, DF_len1, DF_len2, DF_len1
            )

    def test_invalid_est_ind(self):
        with pytest.raises(
            ValueError, match="``wt`` and ``est_ind`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len1, DF_len2, DF_len1, DF_len2, DF_len1
            )

    def test_invalid_est_g2(self):
        with pytest.raises(
            ValueError, match="``est_g2`` and ``se_g2`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len2, DF_len1, DF_len1, DF_len2, DF_len1
            )

    def test_invalid_se_g2(self):
        with pytest.raises(
            ValueError, match="``est_g2`` and ``se_g2`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len2, DF_len2, DF_len1, DF_len1, DF_len1
            )

    def test_invalid_est_g1(self):
        with pytest.raises(
            ValueError, match="``est_g1`` and ``se_g1`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len2, DF_len2, DF_len2, DF_len2, DF_len1
            )

    def test_invalid_se_g1(self):
        with pytest.raises(
            ValueError, match="``est_g1`` and ``se_g1`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len2, DF_len2, DF_len1, DF_len2, DF_len2
            )

    def test_target_lt_aggregate(self):
        with pytest.raises(
            ValueError,
            match="target-level input must be GT aggregate-level input in length.",
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len1, DF_len1, DF_len1, DF_len2, DF_len1, DF_len2
            )

    def test_target_leq_aggregate(self):
        with pytest.raises(
            ValueError,
            match="target-level input must be GT aggregate-level input in length.",
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR, ARRAY_len2, DF_len2, DF_len2, DF_len2, DF_len2, DF_len2
            )

    def test_invalid_g1_shape(self):
        with pytest.raises(
            ValueError, match="``g1`` and ``g2`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                g1=SERIES_len2,
                g2=SERIES_len1,
            )

    def test_invalid_g2_shape(self):
        with pytest.raises(
            ValueError, match="``g1`` and ``g2`` must be equivalent length."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                g1=SERIES_len1,
                g2=SERIES_len2,
            )

    def test_invalid_g1_absent(self):
        with pytest.raises(
            ValueError, match="``g1`` and ``g2`` must both be present or not present."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                g1=None,
                g2=SERIES_len2,
            )

    def test_invalid_g2_absent(self):
        with pytest.raises(
            ValueError, match="``g1`` and ``g2`` must both be present or not present."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                g1=SERIES_len1,
                g2=None,
            )

    def test_invalid_tr_iter_zero(self):
        with pytest.raises(
            ValueError, match="inner trust region iterations must be 1 or greater."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                tr_iter=0,
            )

    def test_invalid_tr_iter_neg1(self):
        with pytest.raises(
            ValueError, match="inner trust region iterations must be 1 or greater."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                tr_iter=-1,
            )

    def test_invalid_tr_tol_low(self):
        with pytest.raises(
            ValueError, match="convergence tolerance be GT 0 and LEQ 1."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                tr_tol=-0.01,
            )

    def test_invalid_tr_tol_high(self):
        with pytest.raises(
            ValueError, match="convergence tolerance be GT 0 and LEQ 1."
        ):
            pmedm_legacy.PMEDM(
                pytest.YEAR,
                ARRAY_len2,
                DF_len2,
                DF_len2,
                DF_len1,
                DF_len2,
                DF_len1,
                tr_tol=1.001,
            )


class TestPMEDMParallel:
    def test_from_super_tract(self, pup_0100100, pup_0100200):
        mpu = {
            pytest.data_0100100["puma_fips"]: pup_0100100,
            pytest.data_0100200["puma_fips"]: pup_0100200,
        }

        pmds = pmedm_legacy.parallel.parallel_solve(mpu, tr_iter=50, tr_tol=1e-3)

        for puma_fips, pmd in pmds.items():
            pup = mpu[puma_fips]

            observed_almat = pmd.pmedm_res["almat"]
            assert observed_almat.dtype == float
            assert observed_almat.shape == (pup.wt.shape[0], pup.est_g2.shape[0])

            observed_serialno = pmd.pmedm_res["serialno"]
            assert observed_serialno.dtype == "<U13"
            assert observed_serialno.shape == (pup.wt.shape[0],)

            observed_geoid = pmd.pmedm_res["geoid"]
            assert observed_geoid.dtype == "<U11"
            assert observed_geoid.shape == (pup.est_g2.shape[0],)

    def test_make_solve(self, pup_0100100):
        pmd = pmedm_legacy.parallel.make_solve(pup_0100100, tr_iter=50, tr_tol=1e-3)

        observed_almat = pmd.pmedm_res["almat"]
        assert observed_almat.dtype == float
        assert observed_almat.shape == (
            pup_0100100.wt.shape[0],
            pup_0100100.est_g2.shape[0],
        )

        observed_serialno = pmd.pmedm_res["serialno"]
        assert observed_serialno.dtype == "<U13"
        assert observed_serialno.shape == (pup_0100100.wt.shape[0],)

        observed_geoid = pmd.pmedm_res["geoid"]
        assert observed_geoid.dtype == "<U11"
        assert observed_geoid.shape == (pup_0100100.est_g2.shape[0],)
