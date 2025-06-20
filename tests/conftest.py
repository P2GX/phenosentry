import os
import pytest

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
def fpath_strict_fail(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "strict-fail-phenopacket.json")

@pytest.fixture(scope="session")
def fpath_default_fail(
    fpath_test_data: str,
) -> str:
    return os.path.join(fpath_test_data, "default-fail-phenopacket.json")

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