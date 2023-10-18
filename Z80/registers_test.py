import hypothesis.strategies as st
from hypothesis import given
from CPU import Registers

@pytest.fixture(scope="session")
def make_registers():
    def make():
        return Registers(AF=0, BC=0, DE=0, HL=0, PC=0, SP=0)
    return make

@given(
    value=st.integers(min_value=0, max_value=0xFF),
    field=st.sampled_from(sorted(REGISTERS_HIGH.items())),
)
def test_registers_high(make_registers, field, value):
    registers = make_registers()
    high_register, full_register = field
    registers[high_register] = value
    assert registers[full_register] == value << 8

