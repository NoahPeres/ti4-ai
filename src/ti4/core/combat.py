"""Combat system for TI4."""

from .system import System


class CombatDetector:
    """Detects when combat should be initiated."""

    def __init__(self) -> None:
        """Initialize the combat detector."""
        pass

    def should_initiate_combat(self, system: System) -> bool:
        """Check if combat should be initiated in a system."""
        # Get all owners of units in the system
        owners = set()
        for unit in system.space_units:
            owners.add(unit.owner)

        # Combat occurs if there are units from different owners
        return len(owners) > 1


class CombatInitiator:
    """Initiates and manages combat encounters."""

    def __init__(self) -> None:
        """Initialize the combat initiator."""
        pass

    def get_combat_participants(self, system: System) -> dict[str, list]:
        """Get combat participants grouped by owner."""
        participants: dict[str, list] = {}

        for unit in system.space_units:
            owner = unit.owner
            if owner not in participants:
                participants[owner] = []
            participants[owner].append(unit)

        return participants
