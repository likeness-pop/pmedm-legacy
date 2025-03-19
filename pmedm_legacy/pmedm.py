# ruff: noqa: E721

import numpy as np
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import IntVector, pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

PMEDMrcpp = importr("PMEDMrcppPal")


class PMEDM:
    """P-MEDM class."""

    def __init__(
        self,
        year: int,
        wt: np.ndarray,
        est_ind: pd.DataFrame,
        est_g2: pd.DataFrame,
        est_g1: pd.DataFrame,
        se_g2: pd.DataFrame,
        se_g1: pd.DataFrame,
        include_cg0: bool = True,
        g1: None | pd.Series = None,
        g2: None | pd.Series = None,
        tr_iter: None | int = None,
        tr_tol: None | float = None,
    ):
        """

        Parameters
        ----------
        year : int
            ACS vintage year.
        wt : numpy.ndarray
            Sample weights. The length of this array *must* equal the number of records
            in ``est_ind``, ``est_g2``, ``se_g2``, and ``g1``/``g2`` (if provided).
        est_ind : pandas.DataFrame
            Individual-level constraints. The number of records *must* equal the
            length of ``wt``, and the number of records in ``est_g2``,
            ``se_g2``, and ``g1``/``g2`` (if provided).
        est_g2 : pandas.DataFrame
            Target-level constraints. The number of records *must* equal the
            length of ``wt``, and the number of records in ``est_ind``,
            ``se_g2``, and ``g1``/``g2`` (if provided).
        est_g1 : pandas.DataFrame
            Aggregate-level constraints. The number of records *must* equal
            the number of records in ``se_g1``.
        se_g2 : pandas.DataFrame
            Target-level standard errors. The number of records *must* equal the
            length of ``wt``, and the number of records in ``est_ind``,
            ``est_g2``, and ``g1``/``g2`` (if provided).
        se_g1 : pandas.DataFrame
            Aggregate-level standard errors. The number of records *must* equal
            the number of records in ``est_g1``.
        include_cg0 : bool = True
            Whether to include Level 0 (PUMA) constraints.
        g1 : None | pandas.Series = None
            Aggregate zone IDs. The number of records *must* equal ``g2``.
        g2 : None | pandas.Series = None
            Target zone IDs. The number of records *must* equal ``g1``.
        tr_iter : None | int = None
            Maximum number of inner trust region iterations.
            ``PMEDMrcpp`` solver defaults to 1000.
        tr_tol : None | float = None
            Convergence tolerance for stopping the solver.
            ``PMEDMrcpp`` solver defaults to 1e-8.

        Attributes
        ----------
        pmedm_res : dict[str, numpy.ndarray]
            A dictionary containing –
                * ``'almat'`` - P-MEDM allocation matrix
                * ``'serialno'`` – PUMS serials
                * ``'geoid'`` – target zone IDs
        """

        # sanity checks ------------------------------------------------
        # year must be integer
        if not isinstance(year, int):
            raise ValueError("``year`` must be an integer.")

        # weights and individuals-level constraints must be equivalent in size
        if wt.shape[0] != est_ind.shape[0]:
            raise ValueError("``wt`` and ``est_ind`` must be equivalent length.")

        # target level input must be equivalent in size
        if est_g2.shape[0] != se_g2.shape[0]:
            raise ValueError("``est_g2`` and ``se_g2`` must be equivalent length.")

        # aggregate level input must be equivalent in size
        if est_g1.shape[0] != se_g1.shape[0]:
            raise ValueError("``est_g1`` and ``se_g1`` must be equivalent length.")

        # target level input must be greater than aggregate level input in size
        if not est_g2.shape[0] > est_g1.shape[0]:
            raise ValueError(
                "target-level input must be GT aggregate-level input in length."
            )

        # zone IDs input must be:
        # 1. both present or both not present;
        # 2. equivalent in size
        has_g1_ids = isinstance(g1, pd.Series)
        has_g2_ids = isinstance(g2, pd.Series)
        if has_g1_ids and has_g2_ids:  # noqa: SIM102
            if g1.shape[0] != g2.shape[0]:
                raise ValueError("``g1`` and ``g2`` must be equivalent length.")
        elif not has_g1_ids and not has_g2_ids:
            pass
        else:
            raise ValueError("``g1`` and ``g2`` must both be present or not present.")

        # inner trust region iterations must be 1 or greater if specified
        if isinstance(tr_iter, int) and tr_iter < 1:
            raise ValueError("inner trust region iterations must be 1 or greater.")

        # convergence tolerance be GT 0 and LEQ 1 if specified
        if tr_tol and (tr_tol <= 0 or tr_tol >= 1):
            raise ValueError("convergence tolerance be GT 0 and LEQ 1.")

        # attribution --------------------------------------------------
        self.year = year
        self.wt = wt
        self.est_ind = est_ind
        self.est_g2 = est_g2
        self.est_g1 = est_g1
        self.se_g2 = se_g2
        self.se_g1 = se_g1
        self.include_cg0 = include_cg0
        self.g1 = g1
        self.g2 = g2
        self.tr_iter = tr_iter
        self.tr_tol = tr_tol

        if self.g1 is None:
            self.g1 = ro.r("NULL")

        if self.g2 is None:
            self.g2 = ro.r("NULL")

        if self.tr_iter is None:
            self.tr_iter = ro.r("NULL")

        if self.tr_tol is None:
            self.tr_tol = ro.r("NULL")

    def solve(self):
        """Solve a ``pmedm_legacy.PMEDM`` instance."""

        # convert pd.DataFrame objects
        with localconverter(ro.default_converter + pandas2ri.converter):
            r_cind = ro.conversion.py2rpy(self.est_ind)
            r_cg2 = ro.conversion.py2rpy(self.est_g2)
            r_cg1 = ro.conversion.py2rpy(self.est_g1)
            r_sg2 = ro.conversion.py2rpy(self.se_g2)
            r_sg1 = ro.conversion.py2rpy(self.se_g1)
            r_include_cg0 = ro.conversion.py2rpy(self.include_cg0)

            if type(self.g1) != "rpy2.rinterface_lib.sexp.NULLType":
                r_g1 = ro.conversion.py2rpy(self.g1)

            if type(self.g2) != "rpy2.rinterface_lib.sexp.NULLType":
                r_g2 = ro.conversion.py2rpy(self.g2)

            if type(self.tr_iter) != "rpy2.rinterface_lib.sexp.NULLType":
                r_tr_iter = ro.conversion.py2rpy(self.tr_iter)

            if type(self.tr_tol) != "rpy2.rinterface_lib.sexp.NULLType":
                r_tr_tol = ro.conversion.py2rpy(self.tr_tol)

        # convert sample weights to R integer vector
        r_wt = IntVector(self.wt.tolist())

        r_pmedm_res = PMEDMrcpp.pmedm(
            r_wt,
            r_cind,
            r_cg2,
            r_cg1,
            r_sg2,
            r_sg1,
            r_include_cg0,
            r_g1,
            r_g2,
            r_tr_iter,
            r_tr_tol,
        )

        # convert PMEDMrcpp outputs to numpy ndarray
        self.pmedm_res = {}

        for key in r_pmedm_res.names:
            obj = r_pmedm_res.rx2(key)

            if type(obj) == ro.vectors.StrVector:
                self.pmedm_res[key] = np.array([i for i in obj])  # noqa: C416

            elif type(obj) == ro.vectors.FloatMatrix:
                self.pmedm_res[key] = np.array(obj)
