import logging
import os
from pathlib import Path
from phenosentry.model import PhenopacketInfo, ZipPhenopacketInfo
from phenosentry.io import read_phenopacket, read_phenopackets, read_cohort
import zipfile

class TestReader:
    logger = logging.getLogger("phenosentry")

    def test_read_phenopacket_eager(
        self,
        fpath_healthy_phenopacket: str
    ):
        phenopacket_info = read_phenopacket(Path(fpath_healthy_phenopacket), self.logger)
        assert isinstance(phenopacket_info, PhenopacketInfo)
        assert phenopacket_info.path == fpath_healthy_phenopacket
        assert phenopacket_info.phenopacket.id == "PMID_28239884_Family_1_proband"

    def test_read_phenopacket_lazy(self, fpath_test_data, fpath_healthy_phenopacket_zip):
        with zipfile.ZipFile(os.path.join(fpath_test_data, "healthy.zip")) as zf:
            for zpath in zf.namelist():
                phenopacket_info = read_phenopacket(zipfile.Path(zf, zpath), self.logger, lazy=True)
                assert isinstance(phenopacket_info, ZipPhenopacketInfo)
                phenopacket = phenopacket_info.phenopacket
                assert phenopacket.id == "PMID_28239884_Family_1_proband"

    def test_read_phenopackets(
            self,
            fpath_ps_folder: str
    ):
        phenopackets = read_phenopackets(Path(fpath_ps_folder), self.logger)
        assert len(phenopackets) == 4

    def test_read_phenopackets_zip(
            self,
            fpath_ps_folder_zip: str):
        with zipfile.ZipFile(fpath_ps_folder_zip) as zf:
            zpath = zipfile.Path(zf)
            phenopackets_lazy = read_phenopackets(zpath, self.logger, lazy=True)
            assert len(phenopackets_lazy) == 4
            print(phenopackets_lazy)
            assert phenopackets_lazy[0].phenopacket.id == "PMID_28239884_Family_2_proband"
            phenopackets = read_phenopackets(zpath, self.logger, lazy=False)
            assert len(phenopackets) == 4

    def test_read_cohort(
            self,
            fpath_ps_folder: str
    ):
        cohort = read_cohort(Path(fpath_ps_folder), self.logger)
        assert cohort.name == "phenopackets"
        assert len(cohort.phenopackets) == 4

    def test_read_cohort_zip(
            self,
            fpath_ps_folder_zip: str
    ):
        with zipfile.ZipFile(fpath_ps_folder_zip) as zf:
            zpath = zipfile.Path(zf)
            cohort = read_cohort(zpath, self.logger)
            assert cohort.name == "phenopackets"
            assert len(cohort.phenopackets) == 4
