"""Integration tests for the keyer module."""
from numpy.lib.arraysetops import setdiff1d
from enigma.keyer import Keyer
import numpy as np

def test_keyer_int():
    morse_code = ".-   ."
    keyer = Keyer(morse_code)

    # Test that signal is just binary
    assert keyer.signal.size >= 0
    setdiff = np.setdiff1d(keyer.signal, np.array([0,1]))
    assert setdiff.size == 0

    # Check audio array is 16-bit
    assert keyer.audio.dtype.type is np.int16

    # Assert playing doesn't throw exceptions
    keyer.play()