import abc

from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket

from stairval import Auditor

# TODO: reorganize the package structure. The auditors for the top-level Phenopacket Schema elements belong to the top-level of the package.
class PhenopacketAuditor(Auditor[Phenopacket], metaclass=abc.ABCMeta):
    """
    Represents information about a cohort of phenopackets.

    TODO: update the attributes
    Attributes:
        name (str): The name of the cohort.
        path (str): The file path to the cohort directory or file.
        phenopackets (typing.Collection[PhenopacketInfo]): A collection of PhenopacketInfo objects representing the phenopackets in the cohort.
    """
    @abc.abstractmethod
    def id(self) -> str:
        return "default_phenopacket_auditor"