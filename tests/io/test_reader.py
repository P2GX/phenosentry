import os
import zipfile

from pathlib import Path

from phenosentry.io import read_phenopacket, read_phenopackets, read_cohort
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket


class TestReader:
    def test_read_phenopacket_eager(
        self,
        fpath_healthy_phenopacket: str,
    ):
        phenopacket = read_phenopacket(Path(fpath_healthy_phenopacket))
        assert isinstance(phenopacket, Phenopacket)
        assert phenopacket.id == "PMID_28239884_Family_1_proband"

    def test_read_phenopacket_lazy(self, fpath_test_data):
        with zipfile.ZipFile(os.path.join(fpath_test_data, "healthy.zip")) as zf:
            for zpath in zf.namelist():
                phenopacket = read_phenopacket(zipfile.Path(zf, zpath))
                assert isinstance(phenopacket, Phenopacket)
                assert phenopacket.id == "PMID_28239884_Family_1_proband"

    def test_read_phenopackets(
        self,
        fpath_ps_folder: str,
    ):
        phenopackets = list(read_phenopackets(Path(fpath_ps_folder)))

        assert len(phenopackets) == 4

    def test_read_cohort(
        self,
        fpath_ps_folder: str,
    ):
        cohort = read_cohort(Path(fpath_ps_folder))
        assert cohort.id == "phenopackets"
        assert len(cohort.members) == 4

    def test_read_cohort_zip(
        self,
        fpath_ps_folder_zip: str,
    ):
        with zipfile.ZipFile(fpath_ps_folder_zip) as zf:
            zpath = zipfile.Path(zf)
            cohort = read_cohort(zpath)
            assert cohort.id == "phenopackets"
            assert len(cohort.members) == 4
