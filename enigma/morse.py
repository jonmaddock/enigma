"""A Morse code encoder and decoder."""
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
    "0": "-----"
}

class Morse():
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
        print(f"Text: {self.text}")

        for char in self.text:
            self.morse += MORSE_CODE[char]

        print(f"Morse: {self.morse}")