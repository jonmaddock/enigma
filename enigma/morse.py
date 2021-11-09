"""A Morse code encoder and decoder.

Morse code consists of "dits", "dahs" and spaces. A dit or dah is a signal, 
whereas a space is an absensce of signal. A dit is one unit of Morse time (or
beat) a dah is three. Each dit or dah is followed by a space of one dit. Each 
character is followed by a space of three dits, and words are separated by a 
space of seven dits.
"""
from enigma.keyer import Keyer

MORSE_CODE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
}

# Define space (in "dits") at end of characters and words
MORSE_CHAR_SPACE = " " * 3
MORSE_WORD_SPACE = " " * 7


class Morse:
    """Morse code encoder/decoder."""

    def __init__(self):
        """Initialise empty text and Morse attributes."""
        self.text = ""
        self.morse = ""

    def encode(self, text):
        """Encode the input text to Morse.

        :param text: text to convert to Morse
        :type text: str
        """
        self.text = text.upper()
        self.morse = ""
        print(f"Text: {self.text}")

        # Convert each character to Morse, then add end-of-character space
        for char in self.text:
            self.morse += MORSE_CODE[char] + MORSE_CHAR_SPACE

        print(f"Morse: {self.morse}")

    def decode(self, morse):
        """Decode input Morse to text.

        :param morse: input Morse code
        :type morse: str
        """
        self.morse = morse
        self.text = ""
        print(f"Morse: {self.morse}")

        # Play Morse code sound
        keyer = Keyer(self.morse)
        keyer.play()

        # Break up Morse words
        morse_words = self.morse.split(MORSE_WORD_SPACE)
        self.decode_words(morse_words)

        print(f"Text: {self.text}")

    def decode_words(self, morse_words):
        """Decode a list of Morse words.

        :param morse_words: list of Morse words
        :type morse_words: list
        """
        # Split each word into letters and decode them
        for morse_word in morse_words:
            morse_letters = morse_word.split(MORSE_CHAR_SPACE)
            self.decode_letters(morse_letters)

            # Add space after word
            self.text += " "

    def decode_letters(self, morse_letters):
        """Decode a list of Morse letters.

        :param morse_letters: list of Morse letters
        :type morse_letters: list
        """
        for morse_letter in morse_letters:
            # Look up each Morse letter to find text letter
            for key, value in MORSE_CODE.items():
                if value == morse_letter:
                    # Found matching Morse; add corresponding text letter
                    self.text += key
                    break
