import dataclasses
import typing
from .phenopacket_info import PhenopacketInfo
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket

@dataclasses.dataclass
class CohortInfo:
    name: str
    path: str
    phenopackets: typing.Collection[PhenopacketInfo]

    def iter_phenopackets(self) -> typing.Iterator[Phenopacket]:
        return map(lambda pi: pi.phenopacket, self.phenopackets)

    def __len__(self) -> int:
        return len(self.phenopackets)