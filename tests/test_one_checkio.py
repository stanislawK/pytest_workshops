import pytest

from app.checkio import friendly_number


def test_friendly_number():
    """Simplest test for function output."""
    assert friendly_number(102) == '102'
    assert friendly_number(10240) == '10k'
    assert friendly_number(12341234, decimals=1) == '12.3M'
    assert friendly_number(12000000, decimals=3) == '12.000M'
    assert friendly_number(12461, decimals=1) == '12.5k'
    assert friendly_number(1024000000, base=1024, suffix='iB') == '976MiB'


@pytest.mark.parametrize("raw, friendly", [(102, '102'), (10240, '10k')])
def test_friendly_number_parametrized(raw, friendly):
    """Tests will run for all parameters - separete for each one."""
    assert friendly_number(raw) == friendly
