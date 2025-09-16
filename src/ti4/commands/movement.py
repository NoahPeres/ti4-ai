"""Movement command implementation."""

from dataclasses import dataclass
from typing import Optional, Dict, Any

from .base import GameCommand
from ..core.game_state import GameState
from ..core.unit import Unit
from ..core.movement import MovementValidator, MovementExecutor


@dataclass
class MovementCommand(GameCommand):
    """Command for unit movement actions."""
    
    unit: Unit
    from_system_id: str
    to_system_id: str
    player_id: str
    from_location: str = "space"  # "space" or planet name
    to_location: str = "space"  # "space" or planet name
    player_technologies: Optional[set[str]] = None
    transport_ship: Optional[Unit] = None  # For ground force transport
    
    def __post_init__(self):
        """Initialize undo data storage."""
        self._undo_data: Dict[str, Any] = {}
    
    def execute(self, game_state: GameState) -> GameState:
        """Execute the movement command."""
        # Store undo data before execution
        self._undo_data = {
            "unit": self.unit,
            "from_system_id": self.from_system_id,
            "to_system_id": self.to_system_id,
            "from_location": self.from_location,
            "to_location": self.to_location
        }
        
        # For now, return the same state (will be implemented properly later)
        return game_state
    
    def undo(self, game_state: GameState) -> GameState:
        """Undo the movement command."""
        # Restore previous state using undo data
        # For now, return the same state (will be implemented properly later)
        return game_state
    
    def can_execute(self, game_state: GameState) -> bool:
        """Check if movement command can be executed."""
        # Basic validation - always return True for now
        return True
    
    def get_undo_data(self) -> Dict[str, Any]:
        """Get data needed for undo operation."""
        return self._undo_data.copy()
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize command for persistence."""
        return {
            "command_type": "MovementCommand",
            "data": {
                "unit_type": self.unit.unit_type if self.unit else None,
                "from_system_id": self.from_system_id,
                "to_system_id": self.to_system_id,
                "player_id": self.player_id,
                "from_location": self.from_location,
                "to_location": self.to_location,
                "player_technologies": list(self.player_technologies) if self.player_technologies else None,
                "transport_ship_type": self.transport_ship.unit_type if self.transport_ship else None
            }
        }