import CPU
import hypothesis.strategies as st
from hypothesis import given

@pytest.fixture(scope="session")
def make_cpu(make_registers, make_decoder):
    def make(data, pc=0):
        cpu = CPU(registers=make_registers(pc=pc), decoder=make_decoder(data=data))
        return cpu

    return make


@given(count=st.integers(min_value=0, max_value=100))
def test_cpu_execute_nop_and_advance(make_cpu, count):
    cpu = make_cpu(b"\x00" * count)
    assert cpu.registers["PC"] == 0
    cpu.run()
    assert cpu.registers["PC"] == count