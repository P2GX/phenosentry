import abc

from ..model import BasePhenopacketStore
from stairval import Auditor


class PhenopacketStoreAuditor(Auditor[BasePhenopacketStore], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def make_id(self) -> str:
        """
        Get a `str` with the auditor id.
        """
        pass
