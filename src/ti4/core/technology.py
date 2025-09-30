"""Technology system for TI4."""

from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from .constants import Technology as TechnologyEnum
from .constants import UnitType

if TYPE_CHECKING:
    from .constants import Faction


class TechnologyColor(Enum):
    """Technology colors in TI4."""

    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"


class TechnologyCard:
    """Represents a technology card for Rule 34 exhausted mechanics.

    This is a minimal implementation to support Rule 34 testing.
    The main technology system uses TechnologyManager and enums.
    """

    def __init__(self, name: str, ability_text: str) -> None:
        self.name = name
        self.ability_text = ability_text
        self._exhausted = False  # Rule 34: Track exhausted state
        self._passive_abilities: dict[str, Any] = {}

    # Rule 34: Exhausted state mechanics
    def is_exhausted(self) -> bool:
        """Check if this technology card is exhausted."""
        return self._exhausted

    def is_faceup(self) -> bool:
        """Check if this technology card is faceup (readied)."""
        return not self._exhausted

    def exhaust(self) -> None:
        """Exhaust this technology card (flip facedown)."""
        if self._exhausted:
            raise ValueError("Card is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        """Ready this technology card (flip faceup)."""
        self._exhausted = False

    def can_resolve_abilities(self) -> bool:
        """Check if this technology card can resolve abilities."""
        return not self._exhausted

    def use_ability(self) -> str:
        """Use the technology's ability, exhausting the card."""
        if self._exhausted:
            raise ValueError("Cannot use ability on exhausted card")

        self.exhaust()
        # Simple mock implementation for testing
        if "command token" in self.ability_text.lower():
            return "Gained 1 command token"
        return "Ability used"

    # Rule 34.4a: Passive abilities work on exhausted cards
    def add_passive_ability(self, ability_name: str, value: Any) -> None:
        """Add a passive ability to this technology card."""
        self._passive_abilities[ability_name] = value

    def get_passive_ability(self, ability_name: str) -> Optional[Any]:
        """Get a passive ability value (works even when exhausted)."""
        return self._passive_abilities.get(ability_name)


# Legacy Technology dataclass removed - using Technology enum from constants


# Legacy TechnologyTree class removed - replaced by TechnologyManager


class TechnologyManager:
    """Manages technology ownership, research, and validation for players.

    This class implements Rule 90: TECHNOLOGY mechanics including:
    - Technology ownership and deck management (Rules 90.1-90.4)
    - Technology research and prerequisites (Rules 90.9-90.12)
    - Unit upgrade identification (Rule 90.6)
    - Technology color system (Rules 90.7-90.8)
    """

    def __init__(self) -> None:
        """Initialize the technology manager."""
        # Track technologies owned by each player (Rule 90.1)
        self._player_technologies: dict[str, set[TechnologyEnum]] = {}

    def get_player_technologies(self, player_id: str) -> set[TechnologyEnum]:
        """Get all technologies owned by a player.

        Args:
            player_id: The player to get technologies for

        Returns:
            Set of technologies owned by the player

        LRR Reference: Rule 90.1 - Each player places any technology they have gained faceup
        """
        return self._player_technologies.get(player_id, set())

    def gain_technology(self, player_id: str, technology: TechnologyEnum) -> None:
        """Give a technology to a player.

        Args:
            player_id: The player gaining the technology
            technology: The technology being gained

        LRR Reference: Rule 90.1 - Players place gained technology faceup near faction sheet
        """
        if player_id not in self._player_technologies:
            self._player_technologies[player_id] = set()
        self._player_technologies[player_id].add(technology)

    def get_technology_deck(self, player_id: str) -> set[TechnologyEnum]:
        """Get all technologies available in a player's deck (not yet owned).

        Args:
            player_id: The player to get the deck for

        Returns:
            Set of technologies available to research

        LRR Reference: Rule 90.2 - A player does not own any technology card that is in their technology deck
        """
        # Get all available technologies (including new framework technologies)
        all_technologies = {
            TechnologyEnum.CRUISER_II,
            TechnologyEnum.FIGHTER_II,
            TechnologyEnum.GRAVITY_DRIVE,
            TechnologyEnum.CARRIER_II,
            TechnologyEnum.DREADNOUGHT_II,
            TechnologyEnum.DESTROYER_II,
            TechnologyEnum.FLEET_LOGISTICS,
            TechnologyEnum.LIGHT_WAVE_DEFLECTOR,
            TechnologyEnum.PLASMA_SCORING,
            TechnologyEnum.ANTIMASS_DEFLECTORS,
            TechnologyEnum.DARK_ENERGY_TAP,  # New framework technology
        }

        # Remove technologies the player already owns
        owned_technologies = self.get_player_technologies(player_id)
        return all_technologies - owned_technologies

    def can_research_technology(
        self, player_id: str, technology: TechnologyEnum
    ) -> bool:
        """Check if a player can research a specific technology.

        Args:
            player_id: The player attempting to research
            technology: The technology to research

        Returns:
            True if the player can research the technology

        LRR Reference: Rule 90.12 - Player must satisfy each prerequisite by owning one technology of matching color
        """
        # Validate inputs
        if not player_id:
            return False

        # Get player's current technologies
        player_technologies = self.get_player_technologies(player_id)

        # Check if technology is already owned
        if technology in player_technologies:
            return False

        # Check if technology is in the player's deck
        deck = self.get_technology_deck(player_id)
        if technology not in deck:
            return False

        # Check prerequisites
        prerequisites = self.get_technology_prerequisites(technology)
        if not prerequisites:
            return True  # No prerequisites needed

        # Count colors of owned technologies
        owned_colors = [self.get_technology_color(tech) for tech in player_technologies]

        # Check if all prerequisite colors are satisfied
        for required_color in prerequisites:
            if owned_colors.count(required_color) < prerequisites.count(required_color):
                return False

        return True

    def research_technology(self, player_id: str, technology: TechnologyEnum) -> bool:
        """Research a technology for a player.

        Args:
            player_id: The player researching the technology
            technology: The technology to research

        Returns:
            True if research was successful

        LRR Reference: Rule 90.10 - To research technology, player gains that technology card from their deck
        """
        if not self.can_research_technology(player_id, technology):
            return False

        self.gain_technology(player_id, technology)
        return True

    def get_technology_color(self, technology: TechnologyEnum) -> TechnologyColor:
        """Get the color of a technology.

        Args:
            technology: The technology to get the color for

        Returns:
            The color of the technology

        LRR Reference: Rule 90.7 - Each technology has a colored symbol indicating that technology's color
        """
        # IMPORTANT: ALL UNIT UPGRADES HAVE NO COLOR (confirmed rule)
        if self.is_unit_upgrade(technology):
            raise ValueError(
                f"Technology {technology} is a unit upgrade and has no color"
            )

        # CONFIRMED NON-UNIT-UPGRADE TECHNOLOGY DATA - DO NOT MODIFY WITHOUT USER APPROVAL
        confirmed_technology_data = {
            TechnologyEnum.GRAVITY_DRIVE: TechnologyColor.BLUE,  # Blue tech (confirmed)
            TechnologyEnum.ANTIMASS_DEFLECTORS: TechnologyColor.BLUE,  # Blue tech, no prerequisites (confirmed)
            TechnologyEnum.QUANTUM_DATAHUB_NODE: TechnologyColor.YELLOW,  # Yellow tech, Hacan faction (confirmed)
            TechnologyEnum.DARK_ENERGY_TAP: TechnologyColor.BLUE,  # Blue tech, confirmed through framework
            # Note: SPEC_OPS_II is a unit upgrade and has no color
        }

        # Return confirmed data or raise error for unconfirmed technologies
        if technology in confirmed_technology_data:
            return confirmed_technology_data[technology]
        else:
            raise ValueError(
                f"Technology {technology} color not confirmed. Please ask user for specification."
            )

    def get_technology_prerequisites(
        self, technology: TechnologyEnum
    ) -> list[TechnologyColor]:
        """Get the prerequisite colors for a technology.

        Args:
            technology: The technology to get prerequisites for

        Returns:
            List of prerequisite colors

        LRR Reference: Rule 90.8 - Most technology cards have prerequisites displayed as colored symbols
        """
        # CONFIRMED PREREQUISITE DATA - DO NOT MODIFY WITHOUT USER APPROVAL
        confirmed_prerequisites = {
            TechnologyEnum.CRUISER_II: [
                TechnologyColor.YELLOW,
                TechnologyColor.RED,
                TechnologyColor.GREEN,
            ],  # Confirmed: 1Y+1R+1G
            TechnologyEnum.GRAVITY_DRIVE: [TechnologyColor.BLUE],  # Confirmed: 1 Blue
            TechnologyEnum.FIGHTER_II: [
                TechnologyColor.BLUE,
                TechnologyColor.GREEN,
            ],  # Confirmed: 1 Blue + 1 Green
            TechnologyEnum.ANTIMASS_DEFLECTORS: [],  # Confirmed: No prerequisites (Level 0)
            TechnologyEnum.SPEC_OPS_II: [
                TechnologyColor.GREEN,
                TechnologyColor.GREEN,
            ],  # Confirmed: 2x Green (Sol faction tech)
            TechnologyEnum.QUANTUM_DATAHUB_NODE: [
                TechnologyColor.YELLOW,
                TechnologyColor.YELLOW,
                TechnologyColor.YELLOW,
            ],  # Confirmed: 3x Yellow (Hacan faction tech)
            TechnologyEnum.DARK_ENERGY_TAP: [],  # Confirmed: No prerequisites (Level 0), confirmed through framework
        }

        # Return confirmed data or raise error for unconfirmed technologies
        if technology in confirmed_prerequisites:
            return confirmed_prerequisites[technology]
        else:
            raise ValueError(
                f"Technology {technology} prerequisites not confirmed. Please ask user for specification."
            )

    def is_unit_upgrade(self, technology: TechnologyEnum) -> bool:
        """Check if a technology is a unit upgrade.

        Args:
            technology: The technology to check

        Returns:
            True if the technology is a unit upgrade

        LRR Reference: Rule 90.6 - Some technologies are unit upgrades that share a name with a unit
        """
        # CONFIRMED UNIT UPGRADE DATA - DO NOT MODIFY WITHOUT USER APPROVAL
        confirmed_unit_upgrades = {
            TechnologyEnum.CRUISER_II,  # Confirmed: Unit upgrade
            TechnologyEnum.FIGHTER_II,  # Confirmed: Unit upgrade
            TechnologyEnum.SPEC_OPS_II,  # Confirmed: Unit upgrade (Sol faction)
        }

        # For unconfirmed technologies, ask user
        if technology not in {
            TechnologyEnum.CRUISER_II,
            TechnologyEnum.GRAVITY_DRIVE,
            TechnologyEnum.FIGHTER_II,
            TechnologyEnum.ANTIMASS_DEFLECTORS,
            TechnologyEnum.SPEC_OPS_II,
            TechnologyEnum.QUANTUM_DATAHUB_NODE,
            TechnologyEnum.DARK_ENERGY_TAP,  # Confirmed through framework
        }:
            raise ValueError(
                f"Technology {technology} unit upgrade status not confirmed. Please ask user for specification."
            )

        return technology in confirmed_unit_upgrades

    def get_upgraded_unit_type(self, technology: TechnologyEnum) -> UnitType:
        """Get the unit type that a technology upgrades.

        Args:
            technology: The unit upgrade technology

        Returns:
            The unit type that is upgraded

        LRR Reference: Rule 90.6 - Unit upgrades share a name with a unit printed on player's faction sheet
        """
        # CONFIRMED UNIT UPGRADE MAPPING - DO NOT MODIFY WITHOUT USER APPROVAL
        upgrade_mapping = {
            TechnologyEnum.CRUISER_II: UnitType.CRUISER,  # Confirmed
            TechnologyEnum.FIGHTER_II: UnitType.FIGHTER,  # Confirmed
        }

        if technology not in upgrade_mapping:
            raise ValueError(f"Technology {technology} is not a unit upgrade")

        return upgrade_mapping[technology]

    # ========================================
    # TECHNOLOGY SPECIFICATION INTERFACE
    # ========================================

    def add_technology_specification(
        self,
        technology: TechnologyEnum,
        color: TechnologyColor,
        prerequisites: list[TechnologyColor],
        is_unit_upgrade: bool,
        upgraded_unit_type: UnitType | None = None,
    ) -> None:
        """Add a complete technology specification.

        This method should ONLY be called after manual confirmation with the user.

        Args:
            technology: The technology to specify
            color: The technology's color
            prerequisites: List of prerequisite colors
            is_unit_upgrade: Whether this is a unit upgrade
            upgraded_unit_type: The unit type upgraded (if applicable)
        """
        # This method provides a clear interface for adding technology specs
        # Implementation would update the confirmed data dictionaries
        raise NotImplementedError(
            "Technology specifications must be added manually after user confirmation"
        )

    def get_unconfirmed_technologies(self) -> set[TechnologyEnum]:
        """Get all technologies that need manual specification.

        Returns:
            Set of technologies missing confirmed specifications
        """
        all_technologies = {
            TechnologyEnum.CRUISER_II,
            TechnologyEnum.FIGHTER_II,
            TechnologyEnum.GRAVITY_DRIVE,
            TechnologyEnum.CARRIER_II,
            TechnologyEnum.DREADNOUGHT_II,
            TechnologyEnum.DESTROYER_II,
            TechnologyEnum.FLEET_LOGISTICS,
            TechnologyEnum.LIGHT_WAVE_DEFLECTOR,
            TechnologyEnum.PLASMA_SCORING,
            TechnologyEnum.ANTIMASS_DEFLECTORS,
            TechnologyEnum.SPEC_OPS_II,
            TechnologyEnum.QUANTUM_DATAHUB_NODE,
            TechnologyEnum.DARK_ENERGY_TAP,  # New framework technology
        }

        confirmed_technologies = {
            TechnologyEnum.CRUISER_II,
            TechnologyEnum.GRAVITY_DRIVE,
            TechnologyEnum.FIGHTER_II,
            TechnologyEnum.ANTIMASS_DEFLECTORS,
            TechnologyEnum.SPEC_OPS_II,
            TechnologyEnum.QUANTUM_DATAHUB_NODE,
            TechnologyEnum.DARK_ENERGY_TAP,  # Confirmed through new framework
        }

        return all_technologies - confirmed_technologies

    def can_research_faction_technology(
        self, player_id: str, player_faction: "Faction", technology: TechnologyEnum
    ) -> bool:
        """Check if a player can research a technology based on faction restrictions.

        Args:
            player_id: The player attempting to research
            player_faction: The player's faction
            technology: The technology to research

        Returns:
            True if the player can research the technology (faction-wise)

        LRR Reference: Rule 90.11 - A player cannot research a faction technology
        that does not match their faction
        """
        # CONFIRMED FACTION TECHNOLOGY DATA - DO NOT MODIFY WITHOUT USER APPROVAL
        from .constants import Faction

        faction_technologies: dict[Faction, set[TechnologyEnum]] = {
            # Sol Federation faction technologies (manually confirmed)
            Faction.SOL: {
                TechnologyEnum.SPEC_OPS_II,  # Confirmed: Sol faction tech, unit upgrade, 2x green prereq
            },
            # Hacan Emirates faction technologies (manually confirmed)
            Faction.HACAN: {
                TechnologyEnum.QUANTUM_DATAHUB_NODE,  # Confirmed: Hacan faction tech, yellow, 3x yellow prereq
            },
            # Xxcha Kingdom faction technologies
            Faction.XXCHA: set(),  # No faction technologies confirmed yet
        }

        # Check if this is a faction technology
        for faction, techs in faction_technologies.items():
            if technology in techs:
                # This is a faction technology - check if player's faction matches
                return player_faction == faction

        # Not a faction technology (or no faction technologies confirmed yet)
        # Generic technologies can be researched by any player
        return True


class TechnologyEffectSystem:
    """Manages technology effects on game mechanics."""

    def __init__(self, unit_stats_provider: Optional[Any] = None) -> None:
        """Initialize the technology effect system."""
        from .unit_stats import UnitStatsProvider

        self._unit_stats_provider = unit_stats_provider or UnitStatsProvider()

    def register_technology_effect(
        self, technology_name: TechnologyEnum, unit_type: UnitType, stat_modifier: Any
    ) -> None:
        """Register a technology effect on unit stats."""
        self._unit_stats_provider.register_technology_modifier(
            technology_name, unit_type, stat_modifier
        )
