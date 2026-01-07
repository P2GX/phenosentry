#!/usr/bin/env python3
from pathlib import Path

import hpotk

from phenosentry.io import read_phenopacket
from phenosentry.auditor.phenopacket import (
    PhenopacketMetaAuditor,
    NoUnwantedCharactersAuditor,
    DeprecatedTermIdAuditor,
    PhenotypicAbnormalityAuditor,
)

# Read a phenopacket.
path = "data/example-phenopacket.json"
phenopacket = read_phenopacket(path=Path(path))

# Some checks use HPO hierarchy. Therefore, we need to load the HPO.
# HPOTK's ontology store downloads and loads the latest HPO.
store = hpotk.configure_ontology_store()
hpo = store.load_minimal_hpo()

# Meta auditor applies a series of auditors on the phenopacket.
auditor = PhenopacketMetaAuditor(
    auditors=(
        NoUnwantedCharactersAuditor.no_whitespace(),
        DeprecatedTermIdAuditor(hpo),
        PhenotypicAbnormalityAuditor(hpo),
    ),
)

# The issues are written into the notepad
notepad = auditor.prepare_notepad("phenopacket")

# Audit the phenopacket.
auditor.audit(
    item=phenopacket,
    notepad=notepad,
)

# Inspect the notepad for errors.
if notepad.has_errors_or_warnings(include_subsections=True):
    print("Invalid Phenopacket")
    notepad.summarize()
else:
    print("Valid Phenopacket")
