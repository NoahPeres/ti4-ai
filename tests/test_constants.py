"""Test constants and enums for better type safety in tests."""

from enum import Enum


class MockPlayer(Enum):
    """Mock player identifiers for tests."""

    PLAYER_1 = "player1"
    PLAYER_2 = "player2"
    PLAYER_3 = "player3"


class MockSystem(Enum):
    """Mock system identifiers for tests."""

    SYSTEM_1 = "system1"
    SYSTEM_2 = "system2"
    SYSTEM_3 = "system3"
    TEST_SYSTEM = "test_system"


class MockPlanet(Enum):
    """Mock planet identifiers for tests."""

    PLANET_A = "planet_a"
    PLANET_B = "planet_b"
    PLANET_C = "planet_c"
