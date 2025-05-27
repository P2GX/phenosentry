import zipfile

import pytest
from phenosentry.model import DefaultPhenopacketStore, PhenopacketStore
from phenosentry.validation import default_auditor, PhenopacketStoreAuditor


class TestPhenopacketStoreAuditor:

    @pytest.fixture(scope="class")
    def auditor(self) -> PhenopacketStoreAuditor:
        return default_auditor()

    @pytest.fixture(scope="class")
    def phenopacket_store(
        self,
        fpath_ps_release_zip: str,
    ) -> PhenopacketStore:
        with zipfile.ZipFile(fpath_ps_release_zip) as zfh:
            return DefaultPhenopacketStore.from_release_zip(zip_file=zfh, strategy="eager")

    @pytest.fixture(scope="class")
    def phenopacket_folder(
        self,
        fpath_ps_folder: str,
    ) -> PhenopacketStore:
        return DefaultPhenopacketStore.from_folder(fpath_ps_folder)

    @pytest.fixture(scope="class")
    def phenopacket_file(
            self,
            fpath_ps_file: str,
    ) -> PhenopacketStore:
        return DefaultPhenopacketStore.from_file(fpath_ps_file)

    def test_audit_store(
        self,
        auditor: PhenopacketStoreAuditor,
        phenopacket_store: DefaultPhenopacketStore,
    ):
        notepad = PhenopacketStoreAuditor.prepare_notepad("test-ps")
        auditor.audit(
            item=phenopacket_store,
            notepad=notepad,
        )
        assert not notepad.has_errors_or_warnings(include_subsections=False)
        assert notepad.has_errors_or_warnings(include_subsections=True)