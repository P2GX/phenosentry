import typing
from stairval.notepad import Notepad
import hpotk

from ._checks import NoUnwantedCharactersCheck, DeprecatedTermIdCheck, UniqueIdsCheck
from ..model import AuditorLevel, PhenopacketAuditor, CohortAuditor, PhenopacketInfo, CohortInfo

class DefaultPhenopacketAuditor(PhenopacketAuditor):
    """
    `DefaultPhenopacketAuditor` is a default implementation of the `PhenopacketAuditor`.
    It provides a default implementation for the `make_id` method.
    """

    def __init__(
            self,
            checks: typing.Iterable[PhenopacketAuditor],
            id: str = "DefaultPhenopacketAuditor"
    ):
        self._checks = tuple(checks)
        self._id = id

    def audit(
            self,
            item: PhenopacketInfo,
            notepad: Notepad,
    ):
        for check in self._checks:
            sub_notepad = notepad.add_subsection(check.id())
            check.audit(
                item=item,
                notepad=sub_notepad,
            )

    def id(self) -> str:
        return self._id

class DefaultCohortAuditor(CohortAuditor):
    """
    `DefaultCohortAuditor` is a default implementation of the `CohortAuditor`.
    It provides a default implementation for the `id` method.
    """

    def __init__(
            self,
            checks: typing.Iterable[CohortAuditor | PhenopacketAuditor],
            id: str = "DefaultCohortAuditor"
    ):
        self._checks = tuple(checks)
        self._id = id

    def audit(
            self,
            item: CohortInfo,
            notepad: Notepad,
    ):
        for check in self._checks:
            if isinstance(check, PhenopacketAuditor):
                sub_notepad = notepad.add_subsection(check.id())
                for phenopacket_info in item.phenopackets:
                    check.audit(
                        item=phenopacket_info,
                        notepad=sub_notepad,
                    )
            else:
                check.audit(
                    item=item,
                    notepad=notepad,
                )

    def id(self) -> str:
        return self._id

def get_phenopacket_auditor(level = AuditorLevel.DEFAULT) -> PhenopacketAuditor :
    """
        Returns a PhenopacketStoreAuditor with default checks.
    """
    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()
    checks = (NoUnwantedCharactersCheck.no_whitespace(),)
    if level == AuditorLevel.STRICT:
        checks += (DeprecatedTermIdCheck(hpo),)
        return DefaultPhenopacketAuditor(id="StrictPhenopacketAuditor", checks=checks)
    return DefaultPhenopacketAuditor(checks=checks)

def get_cohort_auditor() -> CohortAuditor:
    """
        Returns a PhenopacketStoreAuditor with default checks.
    """
    checks = (get_phenopacket_auditor(), UniqueIdsCheck())
    return DefaultCohortAuditor(checks=checks)