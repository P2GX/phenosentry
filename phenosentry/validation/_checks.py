import typing
from collections import Counter, defaultdict
from stairval.notepad import Notepad
from hpotk.ontology import Ontology
from ..model import PhenopacketInfo, CohortInfo, PhenopacketAuditor, CohortAuditor


# Cohort Level Checks
class UniqueIdsCheck(CohortAuditor):
    """
    Check that phenopacket id is unique within the entire cohort.
    """

    def id(self) -> str:
        return "unique_ids_check"

    def audit(
        self,
        item: CohortInfo,
        notepad: Notepad,
    ):
        id_counter = Counter()
        pp_id2cohort = defaultdict(set)
        for pp_info in item.phenopackets:
            pp_id = pp_info.phenopacket.id
            pp_id2cohort[pp_id].add(item.name)
            id_counter[pp_id] += 1

        repeated = {pp_id: count for pp_id, count in id_counter.items() if count > 1}

        for pp_id, count in repeated.items():
            msg = f"`{pp_id}` is present in {count} cohorts: {pp_id2cohort[pp_id]}"
            notepad.add_error(msg)

# Phenopacket Level Checks
class NoUnwantedCharactersCheck(PhenopacketAuditor):
    """
    Check that phenopacket elements do not include any unwanted characters (e.g. whitespace).
    """

    @staticmethod
    def no_whitespace(
        whitespaces: typing.Iterable['str'] = ("\t", "\n", "\r\n"),
    ) -> "NoUnwantedCharactersCheck":
        return NoUnwantedCharactersCheck(whitespaces)

    def __init__(
        self,
        unwanted: typing.Iterable[str],
    ):
        self._unwanted = set(unwanted)

    def id(self) -> str:
        return "unwanted_characters_check"

    def audit(
        self,
        item: PhenopacketInfo,
        notepad: Notepad,
    ):
            pp_pad = notepad.add_subsection(self.id())
            pp = item.phenopacket
            self._check_unwanted_characters(pp.id, pp_pad.add_subsection("id"))
            _, subject_id_pad = pp_pad.add_subsections("subject", "id")
            self._check_unwanted_characters(pp.subject.id, subject_id_pad)

            # Disease name in diseases and variant interpretations
            disease_pad = pp_pad.add_subsection("disease")
            for i, disease in enumerate(pp.diseases):
                _, _, label_pad = disease_pad.add_subsections(f"#{i}", "term", "label")
                self._check_unwanted_characters(disease.term.label, label_pad)

            interpretation_pad = pp_pad.add_subsection("interpretations")
            for i, interpretation in enumerate(pp.interpretations):
                id_pad = interpretation_pad.add_subsection("id")
                self._check_unwanted_characters(interpretation.id, id_pad)
                _, _, label_pad = interpretation_pad.add_subsections("diagnosis", "disease", "label")
                self._check_unwanted_characters(
                    interpretation.diagnosis.disease.label, label_pad
                )

            # PubMed title
            _, ers_pad = pp_pad.add_subsections("meta_data", "external_references")
            for i, er in enumerate(pp.meta_data.external_references):
                _, er_pad = ers_pad.add_subsections(f"#{i}", "description")
                self._check_unwanted_characters(er.description, er_pad)


    def _check_unwanted_characters(
        self,
        value: str,
        notepad: Notepad,
    ):
        for ch in value:
            if ch in self._unwanted:
                notepad.add_error(f"`{value}` includes a forbidden character `{ch}`")


class DeprecatedTermIdCheck(PhenopacketAuditor):

    """
    Check that all term IDs in the phenopackets do not use deprecated identifiers.
    """

    def __init__(self, ontology: Ontology):
        self.ontology = ontology

    def id(self) -> str:
        return "deprecated_term_id_check"

    def audit(
        self,
        item: PhenopacketInfo,
        notepad: Notepad,
    ):
        pp_pad = notepad.add_subsection(self.id())
        pp = item.phenopacket
        for phenotype in pp.phenotypic_features:
            term = self.ontology.get_term(phenotype.type.id)
            if term is not None and term.is_obsolete or term.identifier.value != phenotype.type.id:
                msg = f"`{pp.id}` has a deprecated term ID `{phenotype.type.id}`"
                pp_pad.add_error(msg)


