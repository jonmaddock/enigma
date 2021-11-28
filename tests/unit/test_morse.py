"""Unit tests for the morse module."""
import pytest
from enigma.morse import Morse
from enigma.keyer import Keyer


@pytest.fixture
def morse():
    """Create an instance of Morse.

    :return: Morse object
    :rtype: enigma.morse.Morse
    """
    morse = Morse()
    return morse


def test_init(morse):
    """Test initialisation of Morse object.

    :param morse: Morse object
    :type morse: enigma.morse.Morse
    """
    assert morse.text == ""
    assert morse.morse == ""


def test_encode(morse):
    """Test Morse.encode().

    :param morse: Morse object
    :type morse: enigma.morse.Morse
    """
    # TODO Need to test spaces too
    morse.encode("test")
    assert morse.morse == "-   .   ...   -   "


def test_decode(morse, monkeypatch):
    """Test Morse.decode().

    :param morse: Morse object
    :type morse: enigma.morse.Morse
    :param monkeypatch: fixture for mocking
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    """

    def do_nothing(*args, **kwargs):
        # Mock function to consume args
        pass

    monkeypatch.setattr(Keyer, "__init__", do_nothing)
    monkeypatch.setattr(Keyer, "play", do_nothing)
    monkeypatch.setattr(Morse, "decode_words", do_nothing)

    morse.decode("-   .   ...   -   ")
    # TODO Nothing to assert yet


def test_decode_words(morse, monkeypatch):
    """Test Morse.decode_words().

    :param morse: Morse object
    :type morse: enigma.morse.Morse
    :param monkeypatch: fixture for mocking
    :type monkeypatch: _pytest.monkeypatch.MonkeyPatch
    """

    def mock_decode_letters(*args, **kwargs):
        morse.text += "test"

    monkeypatch.setattr(morse, "decode_letters", mock_decode_letters)
    morse_words = ["-   .   ...   -   "]
    morse.decode_words(morse_words)

    # Can only assert that a space is added
    assert morse.text == "test "


def test_decode_letters(morse):
    """Test Morse.decode_letters().

    :param morse: Morse object
    :type morse: enigma.morse.Morse
    """
    letters = ["-", ".", "...", "-"]
    morse.decode_letters(letters)
    assert morse.text == "TEST"
