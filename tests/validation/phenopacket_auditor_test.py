import logging, pytest
from pathlib import Path
from phenosentry.io import read_phenopacket
from phenosentry.validation import PhenopacketAuditor, AuditorLevel, get_phenopacket_auditor
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket

class TestPhenopacketAuditor:

    @pytest.fixture(scope="class")
    def auditor(self) -> PhenopacketAuditor:
        return get_phenopacket_auditor()

    @pytest.fixture(scope="class")
    def strict_auditor(self) -> PhenopacketAuditor:
        return get_phenopacket_auditor(level=AuditorLevel.STRICT)

    @pytest.fixture(scope="class")
    def phenopacket_strict_fail(
        self,
        fpath_strict_fail: str,
    ) -> Phenopacket:
        return read_phenopacket(Path(fpath_strict_fail), logging.getLogger())

    @pytest.fixture(scope="class")
    def phenopacket_default_fail(
        self,
        fpath_default_fail: str,
    ) -> Phenopacket:
        return read_phenopacket(Path(fpath_default_fail), logging.getLogger())

    def test_strict_phenopacket(
        self,
        strict_auditor: PhenopacketAuditor,
        auditor: PhenopacketAuditor,
        phenopacket_strict_fail: Phenopacket,
    ):
        notepad = PhenopacketAuditor.prepare_notepad("test-ps")
        auditor.audit(
            item=phenopacket_strict_fail,
            notepad=notepad,
        )
        assert not notepad.has_errors_or_warnings(include_subsections=True)
        strict_auditor.audit(
            item=phenopacket_strict_fail,
            notepad=notepad,
        )
        assert notepad.has_errors_or_warnings(include_subsections=True)

    def test_phenopacket(
        self,
        strict_auditor: PhenopacketAuditor,
        auditor: PhenopacketAuditor,
        phenopacket_default_fail: Phenopacket
    ):
        notepad_strict = PhenopacketAuditor.prepare_notepad("test-ps")
        notepad = PhenopacketAuditor.prepare_notepad("test-ps")
        strict_auditor.audit(
            item=phenopacket_default_fail,
            notepad=notepad_strict,
        )
        assert notepad_strict.has_errors_or_warnings(include_subsections=True)
        auditor.audit(
            item=phenopacket_default_fail,
            notepad=notepad,
        )
        assert notepad.has_errors_or_warnings(include_subsections=True)


