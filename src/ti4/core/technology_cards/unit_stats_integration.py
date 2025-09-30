"""
Unit stats integration for technology cards.

This module provides the integration between technology cards and the unit stats system,
mapping enum-based stat modifications to actual UnitStats objects.
"""

from typing import Any, Union

from ti4.core.constants import UnitStatModification
from ti4.core.unit_stats import UnitStats


class UnitStatModificationMapper:
    """Maps UnitStatModification enums to actual stat changes."""

    # Mapping from UnitStatModification enums to UnitStats field names
    _ENUM_TO_FIELD_MAPPING = {
        # Fundamental properties
        UnitStatModification.COST: "cost",
        UnitStatModification.COMBAT_VALUE: "combat_value",
        UnitStatModification.COMBAT_DICE: "combat_dice",
        UnitStatModification.MOVEMENT: "movement",
        UnitStatModification.CAPACITY: "capacity",
        UnitStatModification.PRODUCTION: "production",
        # Unit abilities
        UnitStatModification.SUSTAIN_DAMAGE: "sustain_damage",
        UnitStatModification.ANTI_FIGHTER_BARRAGE: "anti_fighter_barrage",
        UnitStatModification.BOMBARDMENT: "bombardment",
        UnitStatModification.BOMBARDMENT_VALUE: "bombardment_value",
        UnitStatModification.BOMBARDMENT_DICE: "bombardment_dice",
        UnitStatModification.DEPLOY: "deploy",
        UnitStatModification.PLANETARY_SHIELD: "planetary_shield",
        UnitStatModification.SPACE_CANNON: "space_cannon",
        UnitStatModification.SPACE_CANNON_VALUE: "space_cannon_value",
        UnitStatModification.SPACE_CANNON_DICE: "space_cannon_dice",
        UnitStatModification.HAS_PRODUCTION: "has_production",
    }

    # Fields that should be converted to boolean values
    _BOOLEAN_FIELDS = {
        "sustain_damage",
        "anti_fighter_barrage",
        "bombardment",
        "deploy",
        "planetary_shield",
        "space_cannon",
        "has_production",
    }

    @staticmethod
    def map_modifications_to_unit_stats(
        modifications: dict[UnitStatModification, Union[int, bool]],
    ) -> UnitStats:
        """
        Convert enum-based modifications to UnitStats object.

        Args:
            modifications: Dictionary mapping UnitStatModification enums to values

        Returns:
            UnitStats object with the specified modifications

        Raises:
            ValueError: If an unknown UnitStatModification enum is provided
        """
        if not modifications:
            return UnitStats()

        # Initialize all stats to default values (0 or False)
        stats_kwargs: dict[str, Any] = {
            # Fundamental properties
            "cost": 0,
            "combat_value": None,
            "combat_dice": 0,
            "movement": 0,
            "capacity": 0,
            "production": 0,
            # Unit abilities
            "sustain_damage": False,
            "anti_fighter_barrage": False,
            "bombardment": False,
            "bombardment_value": None,
            "bombardment_dice": 0,
            "deploy": False,
            "planetary_shield": False,
            "space_cannon": False,
            "space_cannon_value": None,
            "space_cannon_dice": 0,
            "has_production": False,
        }

        # Apply modifications based on enum values
        for modification, value in modifications.items():
            if not isinstance(modification, UnitStatModification):
                raise ValueError(f"Invalid modification type: {type(modification)}")

            field_name = UnitStatModificationMapper._ENUM_TO_FIELD_MAPPING.get(
                modification
            )
            if field_name is None:
                raise ValueError(f"Unknown UnitStatModification: {modification}")

            # Convert to boolean if needed
            if field_name in UnitStatModificationMapper._BOOLEAN_FIELDS:
                stats_kwargs[field_name] = bool(value)
            else:
                stats_kwargs[field_name] = value

        return UnitStats(**stats_kwargs)
