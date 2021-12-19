"""Unit tests for keyer module."""
import pytest
import numpy as np
from enigma.keyer import Keyer


def mock_signal(*args):
    """Mock creation of a binary signal array.

    :return: binary array
    :rtype: np.ndarray
    """
    signal = np.array([1, 0, 1])
    return signal


def mock_audio(*args):
    """Return random 16-bit audio array.

    :return: 16-bit audio array
    :rtype: np.ndarray
    """
    audio = np.random.rand(3)
    return audio.astype(np.int16)


@pytest.fixture
def keyer(monkeypatch):
    """Create an instance of Keyer.

    :param monkeypatch: fixture for mocking
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    :return: Keyer object
    :rtype: enigma.keyer.Keyer
    """
    monkeypatch.setattr(Keyer, "create_binary_signal", mock_signal)
    monkeypatch.setattr(Keyer, "convert_audio", mock_audio)

    morse_code = ".-   ."
    keyer = Keyer(morse_code)
    return keyer


def test_init(keyer):
    """Test instantiation of Keyer.

    :param keyer: Keyer object
    :type keyer: enigma.keyer.Keyer
    """
    # Test attributes set by mocked methods
    # Test morse converted to binary
    signal_exp = np.array([1, 0, 1])
    np.testing.assert_array_equal(keyer.signal, signal_exp)

    # Test morse converted to 16-bit audio array
    assert keyer.audio.dtype == np.dtype("int16")


def test_create_binary_signal(monkeypatch):
    """Test morse to binary conversion.

    :param monkeypatch: fixture for mocking
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    """
    # Keyer.create_binary_signal() is run in init(); don't mock so it can be
    # tested. Init with empty morse string
    monkeypatch.setattr(Keyer, "convert_audio", mock_audio)
    keyer = Keyer("")

    morse = ".-   ."
    signal_exp = np.array([1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0])
    signal = keyer.create_binary_signal(morse)
    np.testing.assert_array_equal(signal, signal_exp)


def test_convert_audio(monkeypatch):
    """Test conversion of binary to audio.

    :param monkeypatch: fixture for mocking
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    """
    # Keyer.convert_audio() is run in init(); don't mock so it can be
    # tested.
    monkeypatch.setattr(Keyer, "create_binary_signal", mock_signal)
    morse = ".-   ."
    keyer = Keyer(morse)

    # Test morse converted to 16-bit audio array
    # TODO convert_audio() is actually run twice; once in init() and again
    # explicitly. Could this be improved?
    audio = keyer.convert_audio()
    assert audio.dtype == np.dtype("int16")


def test_play(keyer):
    """Check audio can be played.

    :param keyer: Keyer object
    :type keyer: enigma.keyer.Keyer
    """
    # Just check no exceptions are thrown
    keyer.play()
