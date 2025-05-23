from ..model import BasePhenopacketStore, InputMode
import logging

def read_phenopacket_store(
    directory: str, mode: InputMode,
    logger: logging.Logger,
) -> BasePhenopacketStore:
    logger.info("Reading phenopackets at `%s`", directory)
    phenopacket_store = None
    if mode == InputMode.STORE:
        phenopacket_store = BasePhenopacketStore.from_notebook_dir(directory)
    elif mode == InputMode.FOLDER:
        phenopacket_store = BasePhenopacketStore.from_folder(directory)
    elif mode == InputMode.FILE:
        phenopacket_store = BasePhenopacketStore.from_file(directory)
    logger.info(
            "Read %d cohorts with %d phenopackets",
            phenopacket_store.cohort_count(),
            phenopacket_store.phenopacket_count(),
        )
    return phenopacket_store