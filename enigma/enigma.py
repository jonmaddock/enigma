"""An Enigma machine."""

from itertools import cycle
from string import ascii_uppercase as ALPHABET

ROTOR_LEN = len(ALPHABET)


class Enigma:
    """An Enigma machine."""

    def __init__(self):
        """Initialise the machine components."""
        # TODO Implement additional rotors
        self.rotor1 = Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV")

    def press_key(self, letter_input):
        """Press a key on the machine.

        :param letter_input: the key pressed
        :type letter_input: str
        :return: the letter bulb that lights up
        :rtype: str
        """
        # Encode with one rotor to start with
        # Advance rotors with each key press
        self.rotor1.advance()

        # Initial pin index for pressed key; output pin of machine to be input
        # to first rotor (r1)
        # Pin number is relative to position zero of the rotor
        r1_input_pos0 = ALPHABET.find(letter_input)
        # Trace pin through the first rotor
        r1_output_pos0 = self.rotor1.trace(r1_input_pos0)

        # Traced through all rotors: convert final output pin to letter
        letter_output = ALPHABET[r1_output_pos0]
        return letter_output


class Rotor:
    """A single rotor for scrambling an input pin to a different output."""

    def __init__(self, wiring):
        """Wire up each rotor's input/output pins.

        :param wiring: 26 letters representing the wiring order
        :type wiring: str
        """
        # 26 possible positions of rotor
        self.positions = cycle(range(ROTOR_LEN))
        self.wire_up(wiring)
        # Set rotor starting position to 0
        self.advance()

    def wire_up(self, output_letter_order):
        """Wire up the rotor.

        Create a dict to implement the input/output wiring of the rotor pins.
        For example:
        "0": "7",
        "1": "17",
        "2": "2"
        :param output_letter_order: order of the 26 output pins
        :type output_letter_order: str
        """
        # Rotor I/O mappings provided in letters originally (e.g. "A": "D")
        # More useful represented in pin numbers (e.g. 0: 3)
        output_pin_order = []
        for letter in output_letter_order:
            output_pin_order.append(ALPHABET.find(letter))

        self.wiring = dict(zip(range(ROTOR_LEN), output_pin_order))

    def advance(self):
        """Advance the rotor."""
        self.position = next(self.positions)

    def trace(self, input_pin_pos0):
        """Trace an input pin through the rotor to an output pin.

        :param input_pin_pos0: input pin from the previous component (machine
        or previous rotor) relative to position 0 of the rotor
        :type input_pin_pos0: int
        :return: output pin relative to position 0 of rotor
        :rtype: int
        """
        # Find actual input pin of rotor used (input pin relative to rotor)
        # Depends on position zero input pin and the rotor position
        input_pin = input_pin_pos0 + self.position

        # Modulo input pin number if greater than rotor length: can go around
        # rotor more than once
        input_pin = input_pin % ROTOR_LEN

        # Trace input pin through to output, relative to rotor
        output_pin = self.wiring[input_pin]

        # Return output pin relative to position 0 of rotor
        # Take into account possibly going around the rotor more than once
        output_pin_pos0 = (output_pin + self.position) % ROTOR_LEN
        return output_pin_pos0
