"""Run enigma."""
from enigma.enigma import Enigma
from pynput import keyboard


def main():
    """Listen for keyboard input, output Enigma encoded letter immediately."""
    enigma = Enigma()

    def on_press(key):
        """Key press handler.

        :param key: pressed key object
        :type key: keyboard.Key
        :return: False to exit keyboard listener
        :rtype: bool
        """
        try:
            key_pressed = key.char.upper()
            bulb_lit = enigma.press_key(key_pressed)
            print(f"{key_pressed} --> {bulb_lit}")
        except AttributeError:
            # Non-alphanumeric key pressed
            # If esc, exit listener by returning False, otherwise ignore
            if key == keyboard.Key.esc:
                return False

    print("Enigma machine. Type to encode letters. Esc to quit.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
