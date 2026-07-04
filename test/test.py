import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_project(dut):
    cocotb.log.info("Start")

    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    cocotb.log.info("Reset")
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    await Timer(90, units="ns")
    dut.rst_n.value = 1

    cocotb.log.info("Test obstacle avoider")

    # Test FORWARD state (no obstacle)
    dut.ui_in.value = 0b00000000  # obstacle=0, too_close=0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.uo_out.value == 0b00000001, f"Expected FORWARD (uo_out=1), got {dut.uo_out.value}"

    # Test TURNING state (obstacle detected)
    dut.ui_in.value = 0b00000001  # obstacle=1, too_close=0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.uo_out.value == 0b00000010, f"Expected TURNING (uo_out=2), got {dut.uo_out.value}"

    # Test STOPPED state (too close)
    dut.ui_in.value = 0b00000011  # obstacle=1, too_close=1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.uo_out.value == 0b00000100, f"Expected STOPPED (uo_out=4), got {dut.uo_out.value}"

    # Test return to FORWARD
    dut.ui_in.value = 0b00000000  # all clear
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.uo_out.value == 0b00000001, f"Expected FORWARD (uo_out=1), got {dut.uo_out.value}"

    cocotb.log.info("All tests passed!")
