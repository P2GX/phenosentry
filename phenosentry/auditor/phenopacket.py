import typing

from hpotk import MinimalOntology
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket
from stairval.notepad import Notepad

from ._api import PhenopacketAuditor


class NoUnwantedCharactersAuditor(PhenopacketAuditor):
    """
    A check to ensure that phenopacket identifiers do not include unwanted characters (e.g., whitespace).

    The following phenopacket fields are checked:

    * id
    * subject > id
    * diseases > # > term > label
    * interpreattions > # > id
    * interpreattions > # > diagnosis > disease > label
    * meta_data > external_references > # > description
    """

    @staticmethod
    def no_whitespace(
        whitespaces: typing.Iterable["str"] = ("\t", "\n", "\r\n"),
    ) -> "NoUnwantedCharactersAuditor":
        return NoUnwantedCharactersAuditor(whitespaces)

    def __init__(
        self,
        unwanted: typing.Iterable[str],
    ):
        self._unwanted = set(unwanted)

    def id(self) -> str:
        return "unwanted_characters_check"

    def audit(
        self,
        item: Phenopacket,
        notepad: Notepad,
    ):
        self._check_unwanted_characters(item.id, notepad.add_subsection("id"))
        _, subject_id_pad = notepad.add_subsections("subject", "id")
        self._check_unwanted_characters(item.subject.id, subject_id_pad)

        # Disease name in diseases and variant interpretations
        diseases_pad = notepad.add_subsection("diseases")
        for i, disease in enumerate(item.diseases):
            _, _, label_pad = diseases_pad.add_subsections(i, "term", "label")
            self._check_unwanted_characters(disease.term.label, label_pad)

        interpretations_pad = notepad.add_subsection("interpretations")
        for i, interpretation in enumerate(item.interpretations):
            itp_pad = interpretations_pad.add_subsection(i)
            id_pad = itp_pad.add_subsection("id")
            self._check_unwanted_characters(interpretation.id, id_pad)
            _, _, label_pad = itp_pad.add_subsections("diagnosis", "disease", "label")
            self._check_unwanted_characters(interpretation.diagnosis.disease.label, label_pad)

        # PubMed title
        _, ers_pad = notepad.add_subsections("meta_data", "external_references")
        for i, er in enumerate(item.meta_data.external_references):
            _, er_pad = ers_pad.add_subsections(i, "description")
            self._check_unwanted_characters(er.description, er_pad)

    def _check_unwanted_characters(
        self,
        value: str,
        notepad: Notepad,
    ):
        reported = set()
        for ch in value:
            if ch in self._unwanted and ch not in reported:
                notepad.add_error("includes an unwanted character '" + ch + "'")
                reported.add(ch)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}(unwanted={sorted(self._unwanted)})"


class DeprecatedTermIdAuditor(PhenopacketAuditor):
    """
    Checks that no HPO term id is deprecated.
    """

    def __init__(
        self,
        hpo: MinimalOntology,
    ):
        self._hpo = hpo

    def id(self) -> str:
        return "deprecated_term_id_check"

    def audit(
        self,
        item: Phenopacket,
        notepad: Notepad,
    ):
        pf_pad = notepad.add_subsection("phenotypic_features")
        for i, phenotype in enumerate(item.phenotypic_features):
            term = self._hpo.get_term(phenotype.type.id)
            if term is not None and (term.is_obsolete or term.identifier.value != phenotype.type.id):
                _, _, id_pad = pf_pad.add_subsections(i, "type", "id")
                id_pad.add_error(f"`{phenotype.type.id}` has been deprecated")

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}(hpo="{self._hpo.version}")'
