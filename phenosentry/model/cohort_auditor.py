import abc

from stairval import Auditor
from ..model import CohortInfo

class CohortAuditor(Auditor[CohortInfo], metaclass=abc.ABCMeta):
    """
    `PhenopacketAuditor` is an abstract base class for auditing a Phenopacket.
    It extends the `Auditor` class and provides a method to make an ID for the auditor.
    """
    @abc.abstractmethod
    def id(self) -> str:
        return "default_cohort_auditor"
