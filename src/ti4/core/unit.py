"""Unit structure for TI4 game pieces."""


class Unit:
    """Represents a game unit with type and owner."""

    def __init__(self, unit_type: str, owner: str):
        self.unit_type = unit_type
        self.owner = owner
