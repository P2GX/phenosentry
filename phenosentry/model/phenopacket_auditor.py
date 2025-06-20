import abc

from stairval import Auditor
from ..model import PhenopacketInfo


class PhenopacketAuditor(Auditor[PhenopacketInfo], metaclass=abc.ABCMeta):
    """
    `PhenopacketAuditor` is an abstract base class for auditing a Phenopacket.
    It extends the `Auditor` class and provides a method to make an ID for the auditor.
    """
    @abc.abstractmethod
    def id(self) -> str:
        return "default_phenopacket_auditor"