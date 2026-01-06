import pytest

from phenopackets.schema.v2 import Cohort, Phenopacket

from phenosentry.auditor.cohort import UniqueIdsAuditor


class TestUniqueIdsAuditor:
    @pytest.fixture(scope="class")
    def auditor(self) -> UniqueIdsAuditor:
        return UniqueIdsAuditor()

    def test_audit(
        self,
        auditor: UniqueIdsAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Cohort(
            members=(
                Phenopacket(id="A"),
                Phenopacket(id="B"),
                Phenopacket(id="C"),
                Phenopacket(id="A"),
            ),
        )

        auditor.audit(item, notepad)

        summary = notepad.summary()

        assert "`A` is not unique in the cohort" in summary

    def test_repr(
        self,
        auditor: UniqueIdsAuditor,
    ):
        assert repr(auditor) == "phenosentry.auditor.cohort.UniqueIdsAuditor()"
