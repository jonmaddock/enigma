# enigma

An attempt to explore the Enigma ciphering system.

This package currently implements a basic Enigma machine and performs basic encryption of input letters.

## Installation

After cloning, enter the project root directory and create and activate your virtualenv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install `enigma` in your venv:
```bash
pip install .
```

## Usage

To run `enigma`, run:
```bash
python -m enigma
```

`enigma` will then encrypt your input. Pressing the same key multiple times will result in different output as the rotors step forward.