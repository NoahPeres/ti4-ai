"""
Law persistence and tracking system for TI4 agenda cards.

This module provides the ActiveLaw data structure and LawManager class
for tracking persistent law effects throughout the game.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .base import BaseAgendaCard


def _validate_non_empty_string(value: str, field_name: str) -> str:
    """Validate that a string is not None or empty after stripping whitespace."""
    if not value or value.strip() == "":
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()


def _validate_positive_integer(value: int, field_name: str) -> None:
    """Validate that an integer is positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be positive")


@dataclass
class GameContext:
    """Context information for checking law applicability."""

    action_type: str
    player_id: str
    additional_data: dict[str, Any] | None = None


@dataclass
class ConflictResolutionResult:
    """Result of law conflict resolution."""

    removed_laws: list[ActiveLaw]
    enacted_law: ActiveLaw
    message: str


@dataclass
class ActiveLaw:
    """Represents a law currently in effect."""

    agenda_card: BaseAgendaCard
    enacted_round: int
    effect_description: str
    elected_target: str | None = None
    trigger_condition: str | None = None

    def __post_init__(self) -> None:
        """Validate ActiveLaw data after initialization."""
        if self.agenda_card is None:
            raise ValueError("agenda_card cannot be None")

        _validate_positive_integer(self.enacted_round, "enacted_round")
        self.effect_description = _validate_non_empty_string(
            self.effect_description, "effect_description"
        )

    def applies_to_context(self, context: GameContext) -> bool:
        """Check if this law applies to the given game context."""
        # Basic implementation - concrete laws should override this
        # For now, match based on simple keywords in effect description
        effect_lower = self.effect_description.lower()
        action_lower = context.action_type.lower()

        # Technology-related laws
        if self._is_technology_related(effect_lower) and "research" in action_lower:
            return True

        # Fleet-related laws
        if "fleet" in effect_lower and (
            "fleet_pool" in action_lower or "fleet_pool_management" in action_lower
        ):
            return True

        # PDS-related laws
        if "pds" in effect_lower and "pds_placement" in action_lower:
            return True

        # Movement-related laws
        if "movement" in effect_lower and "movement" in action_lower:
            return True
        if "wormhole" in effect_lower and "movement" in action_lower:
            return True

        # Combat-related laws
        if "combat" in effect_lower and "combat" in action_lower:
            return True
        if "destroyed" in effect_lower and "combat" in action_lower:
            return True
        if "reinforcements" in effect_lower and "combat" in action_lower:
            return True

        return False

    def _is_technology_related(self, effect_text: str) -> bool:
        """Check if the effect text is technology-related."""
        return "technology" in effect_text or "tech" in effect_text

    def to_dict(self) -> dict[str, Any]:
        """Serialize ActiveLaw to dictionary for persistence."""
        return {
            "agenda_card_name": self.agenda_card.get_name(),
            "enacted_round": self.enacted_round,
            "effect_description": self.effect_description,
            "elected_target": self.elected_target,
            "trigger_condition": self.trigger_condition,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ActiveLaw:
        """Deserialize ActiveLaw from dictionary."""
        # For now, create a minimal law card - this would need registry integration
        from .base import LawCard

        agenda_card = LawCard(data["agenda_card_name"])

        return cls(
            agenda_card=agenda_card,
            enacted_round=data["enacted_round"],
            effect_description=data["effect_description"],
            elected_target=data.get("elected_target"),
            trigger_condition=data.get("trigger_condition"),
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on all fields."""
        if not isinstance(other, ActiveLaw):
            return False
        return (
            self.agenda_card.get_name() == other.agenda_card.get_name()
            and self.enacted_round == other.enacted_round
            and self.effect_description == other.effect_description
            and self.elected_target == other.elected_target
            and self.trigger_condition == other.trigger_condition
        )

    def __hash__(self) -> int:
        """Hash based on all fields."""
        return hash(
            (
                self.agenda_card.get_name(),
                self.enacted_round,
                self.effect_description,
                self.elected_target,
                self.trigger_condition,
            )
        )


class LawManager:
    """Manages active laws and their persistent effects."""

    def __init__(self) -> None:
        """Initialize empty law manager."""
        self._active_laws: list[ActiveLaw] = []

    def get_active_laws(self) -> list[ActiveLaw]:
        """Get all currently active laws."""
        return self._active_laws.copy()

    def get_law_count(self) -> int:
        """Get the number of active laws."""
        return len(self._active_laws)

    def enact_law(
        self,
        agenda_card_or_active_law: BaseAgendaCard | ActiveLaw,
        enacted_round: int | None = None,
        effect_description: str | None = None,
        elected_target: str | None = None,
    ) -> None:
        """Enact a new law."""
        if isinstance(agenda_card_or_active_law, ActiveLaw):
            # Handle ActiveLaw directly
            active_law = agenda_card_or_active_law
        else:
            # Handle BaseAgendaCard with parameters
            if enacted_round is None or effect_description is None:
                raise ValueError(
                    "enacted_round and effect_description required when passing BaseAgendaCard"
                )

            self._validate_enact_law_parameters(
                agenda_card_or_active_law, enacted_round, effect_description
            )

            active_law = ActiveLaw(
                agenda_card=agenda_card_or_active_law,
                enacted_round=enacted_round,
                effect_description=effect_description,
                elected_target=elected_target,
            )

        # Check for conflicts and remove conflicting laws
        conflicts = self.check_law_conflicts(active_law.agenda_card)
        for conflict in conflicts:
            self.remove_law(conflict.agenda_card.get_name())

        self._active_laws.append(active_law)

    def _validate_enact_law_parameters(
        self,
        agenda_card: BaseAgendaCard,
        enacted_round: int,
        effect_description: str,
    ) -> None:
        """Validate parameters for enacting a law."""
        if agenda_card is None:
            raise ValueError("agenda_card cannot be None")

        _validate_positive_integer(enacted_round, "enacted_round")
        _validate_non_empty_string(effect_description, "effect_description")

    def has_active_law(self, law_name: str) -> bool:
        """Check if a law with the given name is active."""
        if not law_name:
            return False

        return any(law.agenda_card.get_name() == law_name for law in self._active_laws)

    def remove_law(self, law_name: str) -> bool:
        """Remove a law from play. Returns True if law was found and removed."""
        self._validate_law_name(law_name)

        for i, law in enumerate(self._active_laws):
            if law.agenda_card.get_name() == law_name:
                del self._active_laws[i]
                return True

        return False

    def _validate_law_name(self, law_name: str) -> None:
        """Validate that law name is not None or empty."""
        if not law_name:
            raise ValueError("law_name cannot be None or empty")

    def get_law_by_name(self, law_name: str) -> ActiveLaw | None:
        """Get an active law by name."""
        if not law_name:
            return None

        for law in self._active_laws:
            if law.agenda_card.get_name() == law_name:
                return law

        return None

    def get_laws_affecting_context(self, context: GameContext) -> list[ActiveLaw]:
        """Get laws that affect a specific game context."""
        return [law for law in self._active_laws if law.applies_to_context(context)]

    def get_laws_enacted_in_round(self, round_number: int) -> list[ActiveLaw]:
        """Get laws enacted in a specific round."""
        return [law for law in self._active_laws if law.enacted_round == round_number]

    def get_laws_enacted_before_round(self, round_number: int) -> list[ActiveLaw]:
        """Get laws enacted before a specific round."""
        return [law for law in self._active_laws if law.enacted_round < round_number]

    def get_minister_card_owner(self, minister_card_name: str) -> str | None:
        """Get the owner (elected target) of a minister card."""
        for law in self._active_laws:
            if law.agenda_card.get_name() == minister_card_name and law.elected_target:
                return law.elected_target
        return None

    def get_active_minister_effects(self, player_id: str) -> list[ActiveLaw]:
        """Get all active minister effects for a specific player."""
        return [
            law
            for law in self._active_laws
            if law.elected_target == player_id
            and "Minister" in law.agenda_card.get_name()
        ]

    def check_law_conflicts(
        self, agenda_card: BaseAgendaCard | None
    ) -> list[ActiveLaw]:
        """Check for laws that would be replaced by the new law."""
        conflicts: list[ActiveLaw] = []

        # Handle None input gracefully
        if agenda_card is None:
            return conflicts

        new_card_name = agenda_card.get_name()

        # Minister cards replace each other - ANY minister conflicts with ANY other minister
        if "Minister" in new_card_name:
            for law in self._active_laws:
                active_card_name = law.agenda_card.get_name()
                # Any minister conflicts with any other minister (including same type)
                if "Minister" in active_card_name:
                    conflicts.append(law)

        return conflicts

    def enact_law_with_conflict_resolution(
        self,
        agenda_card_or_active_law: BaseAgendaCard | ActiveLaw,
        enacted_round: int | None = None,
        effect_description: str | None = None,
        elected_target: str | None = None,
    ) -> ConflictResolutionResult:
        """Enact a law with automatic conflict resolution and detailed messaging."""
        if isinstance(agenda_card_or_active_law, ActiveLaw):
            # Handle ActiveLaw directly
            new_law = agenda_card_or_active_law
            agenda_card = new_law.agenda_card
        else:
            # Handle BaseAgendaCard with parameters
            if enacted_round is None or effect_description is None:
                raise ValueError(
                    "enacted_round and effect_description required when passing BaseAgendaCard"
                )

            self._validate_enact_law_parameters(
                agenda_card_or_active_law, enacted_round, effect_description
            )

            new_law = ActiveLaw(
                agenda_card=agenda_card_or_active_law,
                enacted_round=enacted_round,
                effect_description=effect_description,
                elected_target=elected_target,
            )
            agenda_card = agenda_card_or_active_law

        # Check for conflicts and remove conflicting laws
        conflicts = self.check_law_conflicts(agenda_card)
        removed_laws = []

        for conflict in conflicts:
            if self.remove_law(conflict.agenda_card.get_name()):
                removed_laws.append(conflict)

        # Enact the new law
        self._active_laws.append(new_law)

        # Create descriptive message
        if removed_laws:
            if len(removed_laws) == 1:
                message = f"{new_law.agenda_card.get_name()} replaced {removed_laws[0].agenda_card.get_name()}"
            else:
                removed_names = [law.agenda_card.get_name() for law in removed_laws]
                message = f"{new_law.agenda_card.get_name()} replaced {', '.join(removed_names)}"
        else:
            message = f"{new_law.agenda_card.get_name()} enacted with no conflicts"

        return ConflictResolutionResult(
            removed_laws=removed_laws,
            enacted_law=new_law,
            message=message,
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on active laws."""
        if not isinstance(other, LawManager):
            return False
        return len(self._active_laws) == len(other._active_laws) and all(
            self_law.agenda_card.get_name() == other_law.agenda_card.get_name()
            and self_law.enacted_round == other_law.enacted_round
            and self_law.effect_description == other_law.effect_description
            and self_law.elected_target == other_law.elected_target
            for self_law, other_law in zip(self._active_laws, other._active_laws)
        )

    def __hash__(self) -> int:
        """Hash based on active laws."""
        return hash(
            tuple(
                (
                    law.agenda_card.get_name(),
                    law.enacted_round,
                    law.effect_description,
                    law.elected_target,
                )
                for law in self._active_laws
            )
        )
