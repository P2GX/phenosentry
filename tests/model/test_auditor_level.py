import pytest

from phenosentry.model import AuditorLevel

@pytest.mark.parametrize("test_input,expected", [("default", AuditorLevel.DEFAULT), ("strict", AuditorLevel.STRICT)])
def test_auditor_level(test_input, expected):
    level =  AuditorLevel(test_input)
    assert level == expected