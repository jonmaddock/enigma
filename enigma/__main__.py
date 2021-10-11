"""Run enigma."""
from enigma.morse import Morse

def main():
    """Encode some text as Morse."""
    morse = Morse()
    morse.encode("test")

if __name__ == "__main__":
    main()