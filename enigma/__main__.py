"""Run enigma."""
from enigma.morse import Morse


def main():
    """Encode some text to Morse and back again."""
    morse = Morse()
    morse.encode("test")

    # Decode the Morse code back again
    morse.decode(morse.morse)


if __name__ == "__main__":
    main()
