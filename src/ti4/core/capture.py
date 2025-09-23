"""Capture system for TI4 units.

This module implements Rule 17: CAPTURE mechanics according to the TI4 LRR.
Handles unit capture, faction sheet storage, and return conditions.
"""

from __future__ import annotations

from .constants import UnitType
from .unit import Unit


class CaptureManager:
    """Manages unit capture mechanics according to Rule 17.

    Handles:
    - Capturing units and placing them appropriately (faction sheet vs tokens)
    - Tracking captured units and tokens
    - Returning captured units under specified conditions
    - Validating capture attempts based on game state
    """

    def __init__(self) -> None:
        """Initialize the capture manager."""
        # Track units on each player's faction sheet (Rule 17.1)
        self._faction_sheet_units: dict[str, list[Unit]] = {}

        # Track fighter/infantry tokens on faction sheets (Rule 17.3)
        self._faction_sheet_tokens: dict[str, dict[UnitType, int]] = {}

        # Track which units are captured (for availability checking)
        self._captured_units: set[Unit] = set()

        # Track blockade states (Rule 17.6)
        self._blockade_states: dict[str, list[str]] = {}

        # Track supply tokens (Rule 17.4c)
        self._supply_tokens: dict[UnitType, int] = {}

    def capture_unit(self, unit: Unit, capturing_player: str) -> None:
        """Capture a unit according to Rule 17 mechanics.

        Args:
            unit: The unit to capture
            capturing_player: The player capturing the unit

        Raises:
            ValueError: If unit is already captured or invalid parameters
        """
        # Input validation
        if not unit or not capturing_player:
            raise ValueError("Unit and capturing player must be provided")

        if unit in self._captured_units:
            raise ValueError(f"Unit {unit.id} is already captured")

        # Mark unit as captured
        self._captured_units.add(unit)

        # Handle based on unit type (Rules 17.1 vs 17.3)
        if unit.unit_type in {UnitType.FIGHTER, UnitType.INFANTRY}:
            # Rule 17.3: Fighter/infantry become tokens
            self._add_faction_sheet_token(capturing_player, unit.unit_type)
        else:
            # Rule 17.1: Non-fighter ships/mechs go to faction sheet
            self._add_faction_sheet_unit(capturing_player, unit)

    def get_faction_sheet_units(self, player_id: str) -> list[Unit]:
        """Get units on a player's faction sheet.

        Args:
            player_id: The player whose faction sheet to check

        Returns:
            List of units on the player's faction sheet
        """
        return self._faction_sheet_units.get(player_id, [])

    def get_faction_sheet_tokens(self, player_id: str, unit_type: UnitType) -> int:
        """Get number of tokens of a specific type on a player's faction sheet.

        Args:
            player_id: The player whose faction sheet to check
            unit_type: The type of token to count

        Returns:
            Number of tokens of the specified type
        """
        player_tokens = self._faction_sheet_tokens.get(player_id, {})
        return player_tokens.get(unit_type, 0)

    def is_unit_available_to_owner(self, unit: Unit) -> bool:
        """Check if a unit is available to its original owner.

        Args:
            unit: The unit to check

        Returns:
            True if the unit is available to its owner, False if captured
        """
        return unit not in self._captured_units

    def is_unit_captured(self, unit: Unit) -> bool:
        """Check if a unit is currently captured.

        Args:
            unit: The unit to check

        Returns:
            True if the unit is captured, False otherwise
        """
        return unit in self._captured_units

    def get_captured_units_by_owner(
        self, original_owner: str, capturing_player: str
    ) -> list[Unit]:
        """Get captured units belonging to a specific original owner held by a capturing player.

        Args:
            original_owner: The original owner of the units
            capturing_player: The player who captured the units

        Returns:
            List of captured units belonging to original_owner held by capturing_player
        """
        captured_units = []

        # Check faction sheet units
        faction_units = self.get_faction_sheet_units(capturing_player)
        for unit in faction_units:
            if unit.owner == original_owner:
                captured_units.append(unit)

        return captured_units

    def return_unit(self, unit: Unit, returning_player: str) -> None:
        """Return a captured unit to its original owner.

        Args:
            unit: The unit to return
            returning_player: The player returning the unit

        Raises:
            ValueError: If unit is not captured or invalid parameters
        """
        # Input validation
        if not unit or not returning_player:
            raise ValueError("Unit and returning player must be provided")

        if unit not in self._captured_units:
            raise ValueError(f"Unit {unit.id} is not currently captured")

        # Remove from captured units
        self._captured_units.discard(unit)

        # Remove from faction sheet if it was there
        if returning_player in self._faction_sheet_units:
            if unit in self._faction_sheet_units[returning_player]:
                self._faction_sheet_units[returning_player].remove(unit)

    def _add_faction_sheet_unit(self, player_id: str, unit: Unit) -> None:
        """Add a unit to a player's faction sheet."""
        if player_id not in self._faction_sheet_units:
            self._faction_sheet_units[player_id] = []
        self._faction_sheet_units[player_id].append(unit)

    def can_produce_unit(self, unit: Unit, player_id: str) -> bool:
        """Check if a player can produce a specific unit.

        Args:
            unit: The unit to check for production availability
            player_id: The player attempting to produce the unit

        Returns:
            True if the unit can be produced, False if captured (Rule 17.5)
        """
        # Rule 17.5: Captured units cannot be produced by original owner
        if unit.owner == player_id and unit in self._captured_units:
            return False
        return True

    def can_capture_unit(
        self, unit: Unit, capturing_player: str, target_owner: str
    ) -> bool:
        """Check if a player can capture a unit from another player.

        Args:
            unit: The unit to capture
            capturing_player: The player attempting the capture
            target_owner: The owner of the unit being captured

        Returns:
            True if capture is allowed, False if blocked (e.g., by blockade)
        """
        # Rule 17.6: Blockaded players cannot capture from blockading players
        blockade_info = self._blockade_states.get(capturing_player)
        if blockade_info and target_owner in blockade_info:
            return False
        return True

    def set_blockade_state(
        self, blockaded_player: str, blockading_players: list[str]
    ) -> None:
        """Set blockade state for a player.

        Args:
            blockaded_player: The player being blockaded
            blockading_players: List of players doing the blockading
        """
        self._blockade_states[blockaded_player] = blockading_players

    def return_fighter_infantry_token(
        self, player_id: str, unit_type: UnitType
    ) -> None:
        """Return a fighter or infantry token to the supply.

        Args:
            player_id: The player returning the token
            unit_type: The type of token to return (FIGHTER or INFANTRY)

        Raises:
            ValueError: If invalid parameters or no tokens to return
        """
        # Input validation
        if not player_id:
            raise ValueError("Player ID must be provided")

        if unit_type not in {UnitType.FIGHTER, UnitType.INFANTRY}:
            raise ValueError("Can only return fighter or infantry tokens")

        # Check if player has tokens to return
        current_tokens = self.get_faction_sheet_tokens(player_id, unit_type)
        if current_tokens == 0:
            raise ValueError(
                f"Player {player_id} has no {unit_type.value} tokens to return"
            )

        # Remove token from faction sheet
        self._faction_sheet_tokens[player_id][unit_type] -= 1

        # Add token back to supply
        if unit_type not in self._supply_tokens:
            self._supply_tokens[unit_type] = 0
        self._supply_tokens[unit_type] += 1

    def get_supply_tokens(self, unit_type: UnitType) -> int:
        """Get the number of tokens of a type in the supply.

        Args:
            unit_type: The type of token to count

        Returns:
            Number of tokens in supply
        """
        return self._supply_tokens.get(unit_type, 0)

    def _add_faction_sheet_token(self, player_id: str, unit_type: UnitType) -> None:
        """Add a token to a player's faction sheet."""
        if player_id not in self._faction_sheet_tokens:
            self._faction_sheet_tokens[player_id] = {}
        if unit_type not in self._faction_sheet_tokens[player_id]:
            self._faction_sheet_tokens[player_id][unit_type] = 0
        self._faction_sheet_tokens[player_id][unit_type] += 1
