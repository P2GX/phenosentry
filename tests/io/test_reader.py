import logging
import pytest
from phenosentry.model import PhenopacketInfo, EagerPhenopacketInfo
from phenosentry.io import read_phenopacket, read_phenopackets, read_cohort


class TestReader:
    logger = logging.getLogger("phenosentry")

    @pytest.fixture(scope="class")
    def phenopacket(
        self,
        fpath_broken: str,
    ) -> PhenopacketInfo:
        return EagerPhenopacketInfo.from_path(fpath_broken)

    def test_read_phenopacket(
        self,
        fpath_broken: str
    ):
        phenopacket_info = read_phenopacket(fpath_broken, self.logger)
        assert isinstance(phenopacket_info, PhenopacketInfo)
        assert phenopacket_info.path == fpath_broken
        assert phenopacket_info.phenopacket.id == "PMID_28239884_Family_4_proband"

    def test_read_phenopackets(
            self,
            fpath_ps_folder: str
    ):
        phenopackets = read_phenopackets(fpath_ps_folder, self.logger)
        assert len(phenopackets) == 4

    def test_read_cohort(
            self,
            fpath_ps_folder: str
    ):
        cohort = read_cohort(fpath_ps_folder, self.logger)
        assert cohort.name == "phenopackets"