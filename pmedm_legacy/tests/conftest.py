import ast
import pathlib

import pandas
import pytest

TEST_DIR = pathlib.Path("pmedm_legacy", "tests")
PARQ = "{}.parquet"


# --------------------------------------------------------------
# adding command line options
# ---------------------------


def pytest_addoption(parser):
    """Add custom command line arguments to the testing suite"""

    # flag for local or remote/VM testing
    parser.addoption(
        "--local",
        action="store",
        default="True",
        help="Boolean flag for local or remote/VM testing.",
        choices=("True", "False"),
        type=str,
    )

    # flag for `dev` environment testing (bleeding edge dependencies)
    parser.addoption(
        "--env",
        action="store",
        default="latest",
        help=(
            "Environment type label of dependencies for determining whether certain "
            "tests should be run. Generally we are working with minimum/oldest, "
            "latest/stable, and bleeding edge."
        ),
        type=str,
    )


def pytest_configure(config):
    """Set session attributes."""

    # ``local`` from ``pytest_addoption()``
    pytest.LOCAL = ast.literal_eval(config.getoption("local"))

    # ``env`` from ``pytest_addoption()``
    pytest.ENV = config.getoption("env")
    valid_env_suffix = ["min", "latest", "dev"]
    assert pytest.ENV.split("_")[-1] in valid_env_suffix

    # path to testing
    pytest.TEST_DIR = TEST_DIR

    # parquet file and extension
    pytest.PARQ = PARQ

    pytest.YEAR = 2019

    # -- pre-built test data --------------
    # Lauderdale, Colbert & Franklin Counties – Alabama
    pytest.data_0100100 = data_0100100()
    # Limestone County – Alabama
    pytest.data_0100200 = data_0100200()

    # Helper classes for pseudo instances
    pytest.ShellPUMA = ShellPUMA
    pytest.ShellPMEDM = ShellPMEDM


# --------------------------------------------------------------
# resusable helpers & data preppers
# ---------------------------------


def _load_puma(puma_fips: str) -> dict[str, str | pandas.DataFrame]:
    """Load pre-computed PUMA/PMEDM data."""

    st_fips = puma_fips[:2]
    builder_dir = TEST_DIR / f"buildup_{puma_fips}"
    almat = pandas.read_parquet(builder_dir / PARQ.format("almat")).to_numpy()
    wt = pandas.read_parquet(builder_dir / PARQ.format("wt"))["wt"].to_numpy()
    est_ind = pandas.read_parquet(builder_dir / PARQ.format("est_ind"))
    est_g1 = pandas.read_parquet(builder_dir / PARQ.format("est_g1"))
    est_g2 = pandas.read_parquet(builder_dir / PARQ.format("est_g2"))
    se_g1 = pandas.read_parquet(builder_dir / PARQ.format("se_g1"))
    se_g2 = pandas.read_parquet(builder_dir / PARQ.format("se_g2"))
    g1 = pandas.read_parquet(builder_dir / PARQ.format("g1"))["g1"]
    g2 = pandas.read_parquet(builder_dir / PARQ.format("g2"))["g2"]

    return {
        "puma_fips": puma_fips,
        "st_fips": st_fips,
        "almat": almat,
        "wt": wt,
        "est_ind": est_ind,
        "est_g1": est_g1,
        "est_g2": est_g2,
        "se_g1": se_g1,
        "se_g2": se_g2,
        "g1": g1,
        "g2": g2,
    }


def data_0100100() -> dict[str, str | pandas.DataFrame]:
    """Lauderdale, Colbert & Franklin Counties – Alabama"""
    return _load_puma("0100100")


def data_0100200() -> dict[str, str | pandas.DataFrame]:
    """Limestone County – Alabama"""
    return _load_puma("0100200")


# --------------------------------------------------------------
# Helper classes for pseudo instances
# -----------------------------------


class Shell:
    def __init__(self, fips: str, year: None | int):
        self.fips = fips
        self.year = year


class ShellPUMA(Shell):
    def __init__(self, fips: str, year: int, data: dict):
        super().__init__(fips, year)
        self.wt = data["wt"]
        self.est_ind = data["est_ind"]
        self.est_g1 = data["est_g1"]
        self.est_g2 = data["est_g2"]
        self.se_g1 = data["se_g1"]
        self.se_g2 = data["se_g2"]
        self.g1 = data["g1"]
        self.g2 = data["g2"]


class ShellPMEDM(Shell):
    def __init__(self, fips: str, data: dict):
        super().__init__(fips, None)
        self.pmedm_res = {"almat": data["almat"]}


@pytest.fixture
def pup_0100100():
    return pytest.ShellPUMA(
        pytest.data_0100100["puma_fips"], pytest.YEAR, pytest.data_0100100
    )


@pytest.fixture
def pmd_0100100():
    return pytest.ShellPMEDM(pytest.data_0100100["puma_fips"], pytest.data_0100100)


@pytest.fixture
def pup_0100200():
    return pytest.ShellPUMA(
        pytest.data_0100200["puma_fips"], pytest.YEAR, pytest.data_0100200
    )
