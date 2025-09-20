"""Space Combat implementation for Rule 78.

LRR Reference: Rule 78 - Space Combat
After resolving the "Space Cannon Offense" step of a tactical action,
if two players have ships in the active system, those players must resolve a space combat.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .constants import UnitType
from .system import System
from .unit import Unit


class CombatStep(Enum):
    """Enumeration of space combat steps."""

    BEFORE_COMBAT = "before_combat"
    ANTI_FIGHTER_BARRAGE = "anti_fighter_barrage"
    ANNOUNCE_RETREATS = "announce_retreats"
    ROLL_DICE = "roll_dice"
    ASSIGN_HITS = "assign_hits"
    RETREAT = "retreat"


@dataclass
class CombatRound:
    """Represents a single round of space combat."""
    round_number: int
    current_step: CombatStep
    attacker_id: str
    defender_id: str
    attacker_units: list[Unit]
    defender_units: list[Unit]
    system: "System"
    attacker_announced_retreat: bool = False
    defender_announced_retreat: bool = False
    attacker_hits: int = 0
    defender_hits: int = 0

    def can_use_anti_fighter_barrage(self) -> bool:
        """AFB only in first round and only if any unit has AFB (Rule 78.3b)."""
        if self.round_number != 1:
            return False
        return any(
            u.has_anti_fighter_barrage() for u in (self.attacker_units + self.defender_units)
        )

    def can_defender_announce_retreat(self) -> bool:
        """Defender can announce retreat if not already announced."""
        return not self.defender_announced_retreat

    def can_attacker_announce_retreat(self) -> bool:
        """Attacker retreat disabled under base rules; enable via variant if needed."""
        return False

    def defender_announces_retreat(self) -> None:
        """Defender announces retreat."""
        self.defender_announced_retreat = True

    def attacker_announces_retreat(self) -> None:
        """Attacker announces retreat."""
        self.attacker_announced_retreat = True

    def execute_retreat_step(self, retreat_system: System) -> bool:
        """Execute retreat step - move retreating units to retreat system.

        Note: This implementation assumes the retreat_system is valid/eligible.
        Full retreat eligibility validation (adjacency, ownership, command tokens)
        should be implemented in the calling code per rules 78.4c and 78.7.
        """
        if self.defender_announced_retreat:
            # Move defender units to retreat system
            retreating_units = [u for u in self.defender_units if u.owner == self.defender_id]
            for unit in retreating_units:
                if unit in self.defender_units:
                    self.defender_units.remove(unit)
                # Move between systems
                self.system.remove_unit_from_space(unit)
                retreat_system.place_unit_in_space(unit)
            return True
        elif self.attacker_announced_retreat:
            # Move attacker units to retreat system
            retreating_units = [u for u in self.attacker_units if u.owner == self.attacker_id]
            for unit in retreating_units:
                if unit in self.attacker_units:
                    self.attacker_units.remove(unit)
                self.system.remove_unit_from_space(unit)
                retreat_system.place_unit_in_space(unit)
            return True
        return False

    def get_attacker_dice_count(self) -> int:
        """Total dice from attacker units."""
        return sum(
            u.get_combat_dice() for u in self.attacker_units if u.get_combat_value() is not None
        )

    def get_defender_dice_count(self) -> int:
        """Total dice from defender units."""
        return sum(
            u.get_combat_dice() for u in self.defender_units if u.get_combat_value() is not None
        )

    def assign_hits_to_attacker(self, hits: int) -> None:
        """Assign hits to attacker."""
        self.attacker_hits = hits

    def assign_hits_to_defender(self, hits: int) -> None:
        """Assign hits to defender."""
        self.defender_hits = hits


@dataclass
class SpaceCombatResult:
    """Result of a space combat."""
    attacker_id: str
    defender_id: str
    attacker_units: list[Unit]
    defender_units: list[Unit]
    winner: Optional[str] = None
    loser: Optional[str] = None
    is_draw: bool = False
    rounds_fought: int = 0
    units_destroyed: list[Unit] = field(default_factory=list)


class SpaceCombat:
    """Handles space combat resolution according to Rule 78."""

    def __init__(self, system: System, attacker_id: str, defender_id: str):
        self.system = system
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self.current_round = 0
        self.combat_ended = False
        self.result: Optional[SpaceCombatResult] = None

    def start_combat(self) -> CombatRound:
        """Start the first round of combat."""
        self.current_round = 1
        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        return CombatRound(
            round_number=self.current_round,
            current_step=CombatStep.BEFORE_COMBAT,
            attacker_id=self.attacker_id,
            defender_id=self.defender_id,
            attacker_units=attacker_units,
            defender_units=defender_units,
            system=self.system,
        )

    def should_continue(self) -> bool:
        """Check if combat should continue."""
        if self.combat_ended:
            return False

        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        # Combat continues if both sides have units
        return len(attacker_units) > 0 and len(defender_units) > 0

    def next_round(self) -> CombatRound:
        """Start the next round of combat."""
        self.current_round += 1
        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        return CombatRound(
            round_number=self.current_round,
            current_step=CombatStep.ANNOUNCE_RETREATS,  # Rule 78.8: Next round starts with retreat announcement
            attacker_id=self.attacker_id,
            defender_id=self.defender_id,
            attacker_units=attacker_units,
            defender_units=defender_units,
            system=self.system,
        )

    def end_combat(self, winner: Optional[str] = None) -> SpaceCombatResult:
        """End combat and return result."""
        self.combat_ended = True

        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        # Determine winner according to Rule 78.10
        result_winner = None
        result_loser = None
        is_draw = False

        if len(attacker_units) > 0 and len(defender_units) == 0:
            # Attacker wins
            result_winner = self.attacker_id
            result_loser = self.defender_id
        elif len(defender_units) > 0 and len(attacker_units) == 0:
            # Defender wins
            result_winner = self.defender_id
            result_loser = self.attacker_id
        elif len(attacker_units) == 0 and len(defender_units) == 0:
            # Draw - neither player has ships
            is_draw = True

        self.result = SpaceCombatResult(
            attacker_id=self.attacker_id,
            defender_id=self.defender_id,
            attacker_units=attacker_units,
            defender_units=defender_units,
            winner=result_winner,
            loser=result_loser,
            is_draw=is_draw,
            rounds_fought=self.current_round,
        )

        return self.result

    def is_combat_required(self) -> bool:
        """Check if combat is required between the two players."""
        attacker_has_ships = False
        defender_has_ships = False

        for unit in self.system.space_units:
            if unit.owner == self.attacker_id and self._is_ship(unit):
                attacker_has_ships = True
            elif unit.owner == self.defender_id and self._is_ship(unit):
                defender_has_ships = True

        return attacker_has_ships and defender_has_ships

    def _is_ship(self, unit: Unit) -> bool:
        """Check if unit is a ship (not ground forces)."""
        ship_types = {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.CRUISER_II,
            UnitType.DREADNOUGHT,
            UnitType.DESTROYER,
            UnitType.FLAGSHIP,
            UnitType.FIGHTER,
            UnitType.WAR_SUN,
        }
        return unit.unit_type in ship_types
