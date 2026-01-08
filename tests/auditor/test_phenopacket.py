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
from phenosentry.auditor.phenopacket import (
    AnnotationInconsistencyAuditor,
    HpoTermIsDefinedAuditor,
    DeprecatedTermIdAuditor,
    ExcludedAnnotationPropagationAuditor,
    NoUnwantedCharactersAuditor,
    PhenotypicAbnormalityAuditor,
    PresentAnnotationPropagationAuditor,
)


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


class TestPhenotypicAbnormalityAuditor:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> PhenotypicAbnormalityAuditor:
        return PhenotypicAbnormalityAuditor(hpo)

    def test_audit(
        self,
        auditor: PhenotypicAbnormalityAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0034382",
                        label="Disease remission",
                    ),
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()

        assert "Disease remission [HP:0034382] is not a descendant of Phenotypic abnormality [HP:0000118]" in summary


class TestAnnotationPropagationValidator:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> PresentAnnotationPropagationAuditor:
        return PresentAnnotationPropagationAuditor(hpo)

    def test_audit(
        self,
        auditor: PresentAnnotationPropagationAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001166",
                        label="Arachnodactyly",
                    ),
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001167",
                        label="Abnormal finger morphology",
                    ),
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0100746",
                        label="Macrodactyly of finger",
                    ),
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()

        assert (
            "annotation to Abnormal finger morphology [HP:0001167] (#1) is redundant due to annotation to Arachnodactyly [HP:0001166] (#0)"
            in summary
        )
        assert (
            "annotation to Abnormal finger morphology [HP:0001167] (#1) is redundant due to annotation to Macrodactyly of finger [HP:0100746] (#2)"
            in summary
        )


class TestExcludedAnnotationPropagationAuditor:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> ExcludedAnnotationPropagationAuditor:
        return ExcludedAnnotationPropagationAuditor(hpo)

    def test_audit(
        self,
        auditor: ExcludedAnnotationPropagationAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001166",
                        label="Arachnodactyly",
                    ),
                    excluded=True,
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001167",
                        label="Abnormal finger morphology",
                    ),
                    excluded=True,
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0100746",
                        label="Macrodactyly of finger",
                    ),
                    excluded=True,
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()

        assert (
            "exclusion of Arachnodactyly [HP:0001166] (#0) is redundant due to exclusion of its ancestor Abnormal finger morphology [HP:0001167] (#1)"
            in summary
        )
        assert (
            "exclusion of Macrodactyly of finger [HP:0100746] (#2) is redundant due to exclusion of its ancestor Abnormal finger morphology [HP:0001167] (#1)"
            in summary
        )


class TestAnnotationInconsistencyAuditor:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> AnnotationInconsistencyAuditor:
        return AnnotationInconsistencyAuditor(hpo)

    def test_audit(
        self,
        auditor: AnnotationInconsistencyAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001166",
                        label="Arachnodactyly",
                    ),
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0001167",
                        label="Abnormal finger morphology",
                    ),
                    excluded=True,
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        id="HP:0100746",
                        label="Macrodactyly of finger",
                    ),
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()

        assert (
            "presence of Arachnodactyly [HP:0001166] (#0) is logically inconsistent with exclusion of Abnormal finger morphology [HP:0001167] (#1)"
            in summary
        )
        assert (
            "presence of Macrodactyly of finger [HP:0100746] (#2) is logically inconsistent with exclusion of Abnormal finger morphology [HP:0001167] (#1)"
            in summary
        )


class TestHpoTermIsPresentAuditor:
    @pytest.fixture(scope="class")
    def auditor(
        self,
        hpo: hpotk.MinimalOntology,
    ) -> HpoTermIsDefinedAuditor:
        return HpoTermIsDefinedAuditor(hpo)

    def test_audit_non_existing_term(
        self,
        auditor: HpoTermIsDefinedAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        # Made-up term that should never exist
                        id="HP:9999999999",
                        label="Made-up term",
                    ),
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert notepad.has_errors_or_warnings(include_subsections=True)

        summary = notepad.summary()

        assert "Made-up term [HP:9999999999] is not present in HPO as of version 2024-04-26" in summary

    def test_audit_current_or_obsolete_term(
        self,
        auditor: HpoTermIsDefinedAuditor,
    ):
        notepad = auditor.prepare_notepad("test")

        item = Phenopacket(
            phenotypic_features=(
                PhenotypicFeature(
                    type=OntologyClass(
                        # Current as of HPO `v2024-04-26`.
                        id="HP:0100786",
                        label="Hypersomnia",
                    ),
                ),
                PhenotypicFeature(
                    type=OntologyClass(
                        # Obsolete for Long fingers [HP:0100807] as of HPO `v2024-04-26`.
                        id="HP:0006010",
                        label="Long fingers",
                    ),
                ),
            ),
        )

        auditor.audit(item=item, notepad=notepad)

        assert not notepad.has_errors_or_warnings(include_subsections=True)
