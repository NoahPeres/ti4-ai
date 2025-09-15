"""Planet structure for TI4 systems."""


class Planet:
    """Represents a planet within a system."""

    def __init__(self, name: str, resources: int, influence: int):
        self.name = name
        self.resources = resources
        self.influence = influence
        self.controlled_by = None
        self.units = []

    def set_control(self, player_id: str) -> None:
        """Set the controlling player of this planet."""
        self.controlled_by = player_id

    def place_unit(self, unit) -> None:
        """Place a unit on this planet."""
        self.units.append(unit)

    def remove_unit(self, unit) -> None:
        """Remove a unit from this planet."""
        self.units.remove(unit)
