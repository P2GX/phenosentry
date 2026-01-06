import hpotk
import pytest

from phenopackets.schema.v2 import (
    Diagnosis,
    Disease,
    Individual,
    Interpretation,
    OntologyClass,
    Phenopacket,
    PhenotypicFeature,
)
from phenosentry.auditor.phenopacket import NoUnwantedCharactersAuditor, DeprecatedTermIdAuditor


class TestNoUnwantedCharactersAuditor:
    @pytest.fixture(scope="class")
    def auditor(self) -> NoUnwantedCharactersAuditor:
        return NoUnwantedCharactersAuditor.no_whitespace()

    def test_audit(
        self,
        auditor: NoUnwantedCharactersAuditor,
    ):
        notepad = auditor.prepare_notepad("test")
        leigh_disease = OntologyClass(
            id="MIM:256000",
            label="LEIGH SYNDROME, NUCLEAR; NULS\n",
        )

        item = Phenopacket(
            id="pp\tid",
            subject=Individual(
                id="subject\nid",
            ),
            diseases=(Disease(term=leigh_disease),),
            interpretations=(
                Interpretation(
                    id="interpretation-id",
                    diagnosis=Diagnosis(disease=leigh_disease),
                ),
            ),
        )
        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()
        assert "includes an unwanted character '\t'" in summary
        assert "includes an unwanted character '\n'" in summary

    def test_repr(
        self,
        auditor: NoUnwantedCharactersAuditor,
    ):
        assert (
            repr(auditor)
            == r"phenosentry.auditor.phenopacket.NoUnwantedCharactersAuditor(unwanted=['\t', '\n', '\r\n'])"
        )


class TestDeprecatedTermIdAuditor:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> DeprecatedTermIdAuditor:
        return DeprecatedTermIdAuditor(hpo)

    def test_audit(
        self,
        auditor: DeprecatedTermIdAuditor,
    ):
        pp = Phenopacket()
        pp.phenotypic_features.append(
            PhenotypicFeature(
                type=OntologyClass(
                    id="HP:0000184",
                    label="Everted lower lip vermilion",
                )
            )
        )

        np = auditor.prepare_notepad("test")
        auditor.audit(pp, np)

        assert np.has_errors_or_warnings(include_subsections=True)

        assert "`HP:0000184` has been deprecated" in np.summary()

    def test_repr(
        self,
        auditor: DeprecatedTermIdAuditor,
    ):
        assert repr(auditor) == 'phenosentry.auditor.phenopacket.DeprecatedTermIdAuditor(hpo="2024-04-26")'
