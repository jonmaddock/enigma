"""Integration tests for the enigma module."""
from enigma import enigma as en


def test_rotor():
    """Test Rotor: input/output for a single rotor.

    Checks its output changes as expected as it rotates.
    """
    rotor = en.Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV")
    # Trace 2 input pins through rotor to output pins
    assert rotor.trace(0) == 3  # A traces to D
    assert rotor.trace(21) == 6  # V traces to G

    # Advance rotor relative to machine (to position 1) and repeat
    rotor.advance()
    # Now A traces to M (pin 12) on rotor, N (pin 13) relative to machine
    assert rotor.trace(0) == 13
    # Now V traces to X (pin 23) on rotor, Y (pin 24) relative to machine
    assert rotor.trace(21) == 24

    # Test Z (pin 25) works, now rotor has been advanced by 1
    # Z now traces to D (3) on rotor, which is E (4) relative to machine
    assert rotor.trace(25) == 4


def test_enigma():
    """Test Enigma class: entire Enigma machine.

    Check that pressing a key results in a different letter lighting up each
    time: the rotors are turning.
    """
    enigma = en.Enigma()

    previous_bulb = None
    for i in range(3):
        bulb = enigma.press_key("A")
        assert previous_bulb != bulb
        previous_bulb = bulb
