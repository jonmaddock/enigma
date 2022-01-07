"""Unit tests for the enigma module."""
from enigma import enigma as en
import pytest
from itertools import cycle


class TestEnigma:
    """Tests for the Enigma class."""

    class MockRotor:
        """Mock class for Rotor1/2/3."""

        def __init__(self, *args):
            """Mock init for Rotor."""
            self.position = 0
            self.turnover_notch = 1

        def step(self):
            """Mock advancing the rotor position."""
            self.position += 1

        def trace(self, *args):
            """Mock trace method for tracing I/O pins on rotor.

            :return: output pin number on rotor
            :rtype: int
            """
            return 5

    @pytest.fixture
    def enigma(self, monkeypatch):
        """Mocked fixture for an Enigma instance.

        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        :return: mocked Enigma instance
        :rtype: enigma.enigma.Enigma
        """
        monkeypatch.setattr(en, "Rotor", self.MockRotor)

        enigma = en.Enigma()
        return enigma

    def test_init(self, enigma):
        """Test initialisation of Enigma instance.

        :param enigma: mocked Enigma instance fixture
        :type enigma: enigma.enigma.Enigma
        """
        assert hasattr(enigma, "rotor1")
        assert hasattr(enigma, "rotor2")
        assert hasattr(enigma, "rotor3")

    def test_press_key(self, enigma, monkeypatch):
        """Test pressing a key on the machine.

        Assert the expected bulb lights.
        :param enigma: mocked Enigma instance fixture
        :type enigma: enigma.enigma.Enigma
        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        """
        monkeypatch.setattr(enigma, "step_rotors", lambda: None)

        bulb = enigma.press_key("C")
        assert bulb == "F"

    def test_step_rotors(self, enigma, monkeypatch):
        """Check mocked rotors step and turn over as expected.

        :param enigma: mocked Enigma instance fixture
        :type enigma: enigma.enigma.Enigma
        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        """
        # All mocked rotors will turnover on pin 1
        # Assert only rotor 1 steps first
        assert enigma.rotor1.position == 0
        enigma.step_rotors()
        assert enigma.rotor1.position == 1

        # Assert rotor 2 turns over on second step
        assert enigma.rotor2.position == 0
        enigma.step_rotors()
        assert enigma.rotor2.position == 1
        assert enigma.rotor1.position == 2

        # Set rotor 1 to turn over rotor 2 again
        # Assert rotor 2 turns over rotor 3 this time; all 3 step
        monkeypatch.setattr(enigma.rotor1, "position", 1)
        assert enigma.rotor3.position == 0
        enigma.step_rotors()
        assert enigma.rotor3.position == 1
        assert enigma.rotor2.position == 2
        assert enigma.rotor1.position == 2


class TestRotor:
    """Tests for the Rotor class."""

    @pytest.fixture
    def rotor(self, monkeypatch):
        """Mocked fixture for Rotor instance.

        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        :return: mocked Rotor instance
        :rtype: enigma.enigma.Rotor
        """
        # Mock initialising the starting position
        monkeypatch.setattr(en.Rotor, "step", lambda *args: None)
        monkeypatch.setattr(en.Rotor, "position", 0, raising=False)

        # Mock wiring by wiring up the first 3 input pins of a rotor
        monkeypatch.setattr(en.Rotor, "wire_up", lambda *args: None)
        monkeypatch.setattr(
            en.Rotor, "wiring", {0: 3, 1: 17, 2: 6}, raising=False
        )
        rotor = en.Rotor("ABC", "B")
        return rotor

    def test_init(self, rotor):
        """Test initialisation of Rotor.

        :param rotor: mocked instance of Rotor
        :type rotor: enigma.enigma.Rotor
        """
        # Assert rotor has positions iterator, wiring and turnover notch
        assert next(rotor.positions) == 0
        assert rotor.wiring[1] == 17
        assert rotor.turnover_notch == 1

    def test_wire_up(self, monkeypatch):
        """Test wiring up of rotor.

        Test wire_up(), so don't use rotor fixture with it mocked out. Mock
        __init__() instead here so that wire_up() can be called.
        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        """
        monkeypatch.setattr(en.Rotor, "__init__", lambda *args: None)
        monkeypatch.setattr(
            en.Rotor, "positions", cycle(range(en.ROTOR_LEN)), raising=False
        )
        rotor = en.Rotor()
        rotor.wire_up("DMTWSILRUYQNKFEJCAZBPGXOHV")
        assert rotor.wiring[0] == 3
        assert rotor.wiring[19] == 1

    def test_step(self, monkeypatch):
        """Test advancing the rotor position by one.

        Test step(), so don't use rotor fixture with it mocked out. Mock
        __init__() instead here so that step() can be called.
        :param monkeypatch: mocking fixture
        :type monkeypatch: _pytest.monkeypatch.Monkeypatch
        """
        monkeypatch.setattr(en.Rotor, "__init__", lambda *args: None)
        monkeypatch.setattr(
            en.Rotor, "positions", cycle(range(en.ROTOR_LEN)), raising=False
        )

        rotor = en.Rotor()
        rotor.step()
        assert rotor.position == 0
        rotor.step()
        assert rotor.position == 1

    def test_trace(self, rotor):
        """Test tracing an input pin through to an output pin.

        :param rotor: mocked instance of Rotor
        :type rotor: enigma.enigma.Rotor
        """
        assert rotor.trace(1) == 17
        assert rotor.trace(2) == 6
