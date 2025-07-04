import abc

from stairval import Auditor
from phenopackets.schema.v2.phenopackets_pb2 import Cohort

class CohortAuditor(Auditor[Cohort], metaclass=abc.ABCMeta):
    """
        Base class for auditing cohorts.

        Methods:
            id() -> str: Abstract method to return the unique identifier for the cohort auditor.
    """
    @abc.abstractmethod
    def id(self) -> str:
        return "default_cohort_auditor"
