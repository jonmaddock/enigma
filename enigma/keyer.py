"""A Morse code keyer.

A Morse "key" is a device with a button used to encode the carrier wave with a
Morse signal. Morse operators use these to produce the familiar "dits" and
"dahs" of Morse code. The Keyer class converts dots and dashes into an encoded
carrier waveform and plays it audibly.
"""
import numpy as np
import simpleaudio as sa

# Dit and dah timings
MORSE_DIT_FREQ = 10  # dits per second
MORSE_DIT = 1
MORSE_DAH = 3

# Audio settings
FREQUENCY = 440  # 440 Hz
SAMPLE_RATE = 44100


class Keyer:
    """Convert Morse code to audio and play it."""

    def __init__(self, morse):
        """Convert Morse to playable audio.

        :param morse: dot-and-dash Morse code
        :type morse: str
        """
        self.signal = self.create_binary_signal(morse)
        self.audio = self.convert_audio()

    def create_binary_signal(self, morse):
        """Converts Morse code into a binary signal.

        For example, ".-   ." becomes "1011100001"
        :param morse: dot-and-dash Morse code
        :type morse: str
        :return: binary Morse code signal
        :rtype: np.ndarray
        """
        signal_list = []

        # Convert to binary dit, dah or space
        # Always add a space of one dit
        for char in morse:
            if char == ".":
                signal_list += MORSE_DIT * [1]
            elif char == "-":
                signal_list += MORSE_DAH * [1]

            signal_list += MORSE_DIT * [0]

        # TODO Correct number of spaces: consider end of char/word following
        # dit/dah: has one too many spaces currently

        # signal_list is now list of binary digits, each representing a dit
        # duration of on or off
        signal = np.array(signal_list)
        return signal

    def convert_audio(self):
        """Convert binary signal to audio.

        Encode sine wave with binary signal and create playable audio.
        :return: 16-bit audio waveform
        :rtype: np.ndarray
        """
        # Stretch signal array to match the required sample rate and duration
        samples_per_dit = int(round(SAMPLE_RATE / MORSE_DIT_FREQ))
        signal_stretched = np.repeat(self.signal, samples_per_dit)

        # Create increasing time value array of equivalent length
        duration = signal_stretched.size / SAMPLE_RATE
        t = np.linspace(
            0.0, duration, num=signal_stretched.size, endpoint=False
        )

        # Create a sine wave at 440 Hz
        sine = np.sin(2 * np.pi * FREQUENCY * t)

        # Encode sine wave with signal
        enc_sine = sine * signal_stretched

        # Ensure that sine is in 16-bit range, normalised to maximum amplitude
        audio = (2 ** 15 - 1) * enc_sine / (np.max(np.abs(enc_sine)))

        # Convert to 16-bit data
        audio = audio.astype(np.int16)
        return audio

    def play(self):
        """Play Morse code."""
        # Start playback
        play_obj = sa.play_buffer(self.audio, 1, 2, SAMPLE_RATE)

        # Wait for playback to finish before exiting
        play_obj.wait_done()
