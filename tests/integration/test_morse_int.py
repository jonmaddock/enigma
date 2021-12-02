"""Integration tests for the morse module."""
from enigma.morse import Morse


def test_encode():
    """Test encoding text to Morse code."""
    morse = Morse()
    text = "Testing"
    morse.encode(text)
    assert morse.morse == '-   .   ...   -   ..   -.   --.   '

def test_decode():
    """Test decoding Morse code to text."""
    morse = Morse()
    morse_code = '-   .   ...   -   ..   -.   --.   '
    morse.decode(morse_code)
    # TODO Correct spaces
    assert morse.text == "TESTING "