# import multiprocessing
from multiprocessing import cpu_count, pool

from .pmedm import PMEDM

n_procs = cpu_count() - 1


def make_solve(
    pup,
    include_cg0: bool = True,
    tr_iter: None | int = None,
    tr_tol: None | float = None,
) -> PMEDM:
    """Helper for solving multiple ``PMEDM`` instances.

    Parameters
    ----------
    pup : livelike.acs.puma | pronto_gatto.acs.puma
        PUMA instance.
    include_cg0 : bool = True
        Whether to include Level 0 (PUMA) constraints.
    tr_iter : None | int = None
        Maximum number of inner trust region iterations.
        ``PMEDMrcpp`` solver defaults to 1000.
    tr_tol : None | float = None
        Convergence tolerance for stopping the solver.
        ``PMEDMrcpp`` solver defaults to 1e-8.

    Returns
    -------
    pmd : pmedm_legacy.pmedm.PMEDM
        A solved P-MEDM problem.
    """

    pmd = PMEDM(
        pup.year,
        pup.wt,
        pup.est_ind,
        pup.est_g2,
        pup.est_g1,
        pup.se_g2,
        pup.se_g1,
        g1=pup.g1,
        g2=pup.g2,
        include_cg0=include_cg0,
        tr_iter=tr_iter,
        tr_tol=tr_tol,
    )
    pmd.solve()

    return pmd


def parallel_solve(
    mpu: dict,
    include_cg0: bool = True,
    tr_iter: None | int = None,
    tr_tol: None | float = None,
) -> dict[str, PMEDM]:
    """Solves P-MEDM problems with parallelization.

    Parameters
    ----------
    mpu : dict[str, livelike.acs.puma | pronto_gatto.acs.puma]
        A dictionary of PUMA instances (``livelike.acs.puma``
        or ``pronto_gatto.acs.puma``) keyed by PUMA FIPS codes.
    include_cg0 : bool = True
        Whether to include Level 0 (PUMA) constraints.
    tr_iter : None | int = None
        Maximum number of inner trust region iterations.
        ``PMEDMrcpp`` solver defaults to 1000.
    tr_tol : None | float = None
        Convergence tolerance for stopping the solver.
        ``PMEDMrcpp`` solver defaults to 1e-8.

    Returns
    -------
    pmd : dict[str, pmedm_legacy.pmedm.PMEDM]
        A dictionary of P-MEDM instances with solutions keyed by PUMA FIPS codes.
    """

    pumas = list(mpu.keys())

    specs = tuple(
        zip(
            [v for k, v in mpu.items()],
            [include_cg0] * len(pumas),
            [tr_iter] * len(pumas),
            [tr_tol] * len(pumas),
            strict=True,
        )
    )

    wrk = pool.Pool(n_procs)
    pmds = wrk.starmap(make_solve, specs)
    wrk.close()

    pmds = dict(zip(pumas, pmds, strict=True))

    return pmds
