from ._api import PhenopacketStoreAuditor
from ._checks import DefaultPhenopacketStoreAuditor, UniqueIdsCheck, NoUnwantedCharactersCheck, DeprecatedTermIdCheck
import hpotk

def configure_qc_checker() -> PhenopacketStoreAuditor:
    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()
    checks = (
        UniqueIdsCheck(),
        NoUnwantedCharactersCheck.no_whitespace(),
        DeprecatedTermIdCheck(hpo)
    )
    return DefaultPhenopacketStoreAuditor(checks=checks)