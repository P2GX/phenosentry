import logging, pytest

from phenosentry.io import read_cohort
from phenosentry.model import CohortAuditor, CohortInfo
from phenosentry.validation import get_cohort_auditor


class TestCohortAuditor:

    @pytest.fixture(scope="class")
    def auditor(self) -> CohortAuditor:
        return get_cohort_auditor()

    @pytest.fixture(scope="class")
    def cohort_pass(
            self,
            fpath_healthy_cohort: str,
    ) -> CohortInfo:
        return read_cohort(fpath_healthy_cohort, logging.getLogger())

    @pytest.fixture(scope="class")
    def cohort_fail(
            self,
            fpath_dirty_cohort: str,
    ) -> CohortInfo:
        return read_cohort(fpath_dirty_cohort, logging.getLogger())

    def test_cohort_pass(
            self,
            auditor: CohortAuditor,
            cohort_pass: CohortInfo,
    ):
        notepad = CohortAuditor.prepare_notepad("test-ps")
        auditor.audit(
            item=cohort_pass,
            notepad=notepad,
        )
        assert not notepad.has_errors_or_warnings(include_subsections=False)

    def test_cohort_fail(self, auditor: CohortAuditor, cohort_fail: CohortInfo):
        notepad = CohortAuditor.prepare_notepad("test-ps")
        auditor.audit(
            item=cohort_fail,
            notepad=notepad,
        )
        assert notepad.has_errors_or_warnings(include_subsections=False)


