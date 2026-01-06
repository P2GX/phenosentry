from collections import Counter, defaultdict

from phenopackets.schema.v2.phenopackets_pb2 import Cohort
from stairval.notepad import Notepad

from ._api import CohortAuditor


class UniqueIdsAuditor(CohortAuditor):
    """
    A check to ensure that all phenopacket IDs within a cohort are unique.
    """

    def id(self) -> str:
        return "unique_pp_ids_in_cohort_check"

    def audit(
        self,
        item: Cohort,
        notepad: Notepad,
    ):
        id_counter = Counter()
        pp_id2cohort = defaultdict(set)
        for pp in item.members:
            pp_id2cohort[pp.id].add(item.id)
            id_counter[pp.id] += 1

        repeated = {pp_id: count for pp_id, count in id_counter.items() if count > 1}

        for pp_id, count in repeated.items():
            notepad.add_error(f"`{pp_id}` is not unique in the cohort")

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}()"
