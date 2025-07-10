import os
import pytest
from pathlib import Path
import typing

from google.protobuf.message import Message
from google.protobuf.json_format import Parse

@pytest.fixture(scope="session")
def fpath_test_data() -> str:
    fpath_test_dir = os.path.join(os.getcwd(), "tests")
    return os.path.join(fpath_test_dir, "test_data")

@pytest.fixture(scope="session")
def fpath_ps_folder(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "phenopackets")

@pytest.fixture(scope="session")
def fpath_ps_folder_zip(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "phenopackets.zip")

@pytest.fixture(scope="session")
def fpath_healthy_phenopacket(
    fpath_ps_folder: str,
) -> str:
    return os.path.join(fpath_ps_folder, "PMID_28239884_Family1proband.json")

@pytest.fixture(scope="session")
def fpath_healthy_phenopacket_zip(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "healthy.zip")


@pytest.fixture(scope="session")
def fpath_strict_fail(
    fpath_test_data: str,
) -> Path:
    return Path(os.path.join(fpath_test_data, "strict-fail-phenopacket.json"))

@pytest.fixture(scope="session")
def fpath_default_fail(
    fpath_test_data: str,
) -> Path:
    return Path(os.path.join(fpath_test_data, "default-fail-phenopacket.json"))

@pytest.fixture(scope="session")
def fpath_healthy_cohort(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "cohort_pass")

@pytest.fixture(scope="session")
def fpath_dirty_cohort(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "cohort_fail")


MSG = typing.TypeVar("MSG", bound=Message, covariant=True)


def read_pb_message(fpath: typing.Union[str, Path], msg: MSG) -> MSG:
    with open(fpath) as fh:
        return Parse(fh.read(), msg)
