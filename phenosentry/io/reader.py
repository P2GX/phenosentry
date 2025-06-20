import logging, typing
from ..model import  CohortInfo, PhenopacketInfo, EagerPhenopacketInfo
from pathlib import Path
from google.protobuf.json_format import Parse, ParseError
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket


def read_phenopacket(
    directory: str,
    logger: logging.Logger,
) -> PhenopacketInfo:
    logger.info("Reading phenopacket at `%s`", directory)
    try:
        path = Path(directory)
        pp = Parse(path.read_text(), Phenopacket())
    except ParseError as e:
        logger.error("Failed to parse phenopacket at `%s`: %s", directory, e)
        raise ValueError(f"Invalid phenopacket format in {directory}") from e
    return EagerPhenopacketInfo.from_phenopacket(directory, pp)

def read_phenopackets(directory: str, logger: logging.Logger) -> typing.List[PhenopacketInfo]:
    logger.info("Reading phenopackets at `%s`", directory)
    path = Path(directory)
    phenopackets = []
    for pp_path in path.glob("*.json"):
        phenopackets.append(read_phenopacket(pp_path, logger))
    return phenopackets

def read_cohort(
    directory: str,
    logger: logging.Logger,
) -> CohortInfo:
    logger.info("Reading cohort at `%s`", directory)
    path = Path(directory)
    phenopackets = read_phenopackets(directory, logger)
    return CohortInfo(name=path.name, path=str(path), phenopackets=phenopackets)