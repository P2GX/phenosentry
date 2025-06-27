import zipfile
import pytest, os
from pathlib import Path
from phenosentry.io import read_phenopacket
from phenosentry.model import EagerPhenopacketInfo


# this can be either in a zip or a folder or a file literal, but its just a path to a file, we only care if its eager or lazy
@pytest.mark.parametrize("test_input", ["test_get_store_zip0/AAGAB/PMID_28239884_Family1proband.json", ""])
def test_eager_phenopacket_zip(test_input, fpath_test_data):
    """Test EagerPhenopacketInfo.from_path with a valid phenopacket file in a zip."""
    if ".zip" in test_input:
        with zipfile.ZipFile(os.path.join(fpath_test_data, "test_get_store_zip0.zip")) as z:
            zz = zipfile.Path(z)
            eg = read_phenopacket(zz)
            assert eg.phenopacket.id == "PMID_28239884_Family_1_proband"

@pytest.mark.parametrize("test_input", ["PMID_28239884_Family1proband.json"])
def test_eager_phenopacket(test_input, fpath_ps_folder):
    """Test EagerPhenopacketInfo.from_path with a valid phenopacket file."""

    p = Path(os.path.join(fpath_ps_folder, test_input))
    eg = EagerPhenopacketInfo.from_path(p)
    assert eg
    assert eg.phenopacket.id == "PMID_28239884_Family_1_proband"


@pytest.mark.parametrize("test_input", ["test_get_store_zip0/AAGAB/PMID_28239884_Family1proband.json", ""])
def test_zip_phenopacket(test_input, fpath_test_data):
    """Test EagerPhenopacketInfo.from_path with a valid phenopacket file."""

