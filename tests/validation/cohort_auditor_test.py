from pathlib import Path

import pytest

from phenosentry.io import read_cohort
from phenosentry.validation import CohortAuditor, get_cohort_auditor
from phenopackets.schema.v2.phenopackets_pb2 import Cohort


class TestCohortAuditor:
    @pytest.fixture(scope="class")
    def auditor(self) -> CohortAuditor:
        return get_cohort_auditor()

    @pytest.fixture(scope="class")
    def cohort_pass(
        self,
        fpath_healthy_cohort: str,
    ) -> Cohort:
        return read_cohort(Path(fpath_healthy_cohort))

    @pytest.fixture(scope="class")
    def cohort_fail(
        self,
        fpath_dirty_cohort: str,
    ) -> Cohort:
        return read_cohort(Path(fpath_dirty_cohort))

    def test_cohort_pass(
        self,
        auditor: CohortAuditor,
        cohort_pass: Cohort,
    ):
        notepad = auditor.prepare_notepad("test-ps")
        auditor.audit(
            item=cohort_pass,
            notepad=notepad,
        )
        assert not notepad.has_errors_or_warnings(include_subsections=False)

    def test_cohort_fail(self, auditor: CohortAuditor, cohort_fail: Cohort):
        notepad = CohortAuditor.prepare_notepad("test-ps")
        auditor.audit(
            item=cohort_fail,
            notepad=notepad,
        )
        assert notepad.has_errors_or_warnings(include_subsections=False)
