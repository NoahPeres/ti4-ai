"""Diplomacy Strategy Card implementation for TI4.

This module implements the Diplomacy strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 32 - DIPLOMACY (Strategy Card)
"""

from typing import TYPE_CHECKING, Any, Optional

from ...constants import SystemConstants
from ..base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from ..strategic_action import StrategyCardType

if TYPE_CHECKING:
    from ...game_state import GameState


class DiplomacyStrategyCard(BaseStrategyCard):
    """Implementation of the Diplomacy strategy card.

    LRR Reference: Rule 32 - The "Diplomacy" strategy card.
    This card's initiative value is "2."
    """

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.DIPLOMACY
        """
        return StrategyCardType.DIPLOMACY

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Diplomacy strategy card.

        Returns:
            The initiative value (2)

        LRR Reference: Rule 83 - Diplomacy has initiative value "2"
        """
        return 2

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Diplomacy strategy card.

        LRR 32.2: Choose 1 system other than the Mecatol Rex system that contains
        a planet you control; each other player places a command token from their
        reinforcements in that system. Then, ready up to 2 exhausted planets you control.

        Args:
            player_id: The active player executing the primary ability
            game_state: Game state for full integration
            **kwargs: Additional parameters - expects 'system_id' for the chosen system
                     and optionally 'planets_to_ready' list

        Returns:
            Result of the primary ability execution
        """
        if not game_state:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Game state is required for Diplomacy primary ability",
            )

        system_id = kwargs.get("system_id")
        if not system_id:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="System ID must be provided for Diplomacy primary ability",
            )

        # Rule 32.2: Cannot select Mecatol Rex system
        if system_id == SystemConstants.MECATOL_REX_ID:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Cannot select Mecatol Rex system for Diplomacy primary ability",
            )

        # Validate the system exists and contains a planet controlled by the active player
        if not game_state.galaxy:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Galaxy not found in game state",
            )

        system = game_state.galaxy.get_system(system_id)
        if not system:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"System {system_id} not found",
            )

        # Check if system contains a planet controlled by the active player
        player_controlled_planets = []
        for planet in system.planets:
            if planet.controlled_by == player_id:
                player_controlled_planets.append(planet)

        if not player_controlled_planets:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} does not control any planet in system {system_id}",
            )

        # Rule 32.2: Each other player places one command token from their reinforcements in that system
        other_players = [p for p in game_state.players if p.id != player_id]
        for other_player in other_players:
            # Rule 32.2.b: If player already has a command token in the system, don't place another
            if system.has_command_token(other_player.id):
                continue

            # Try to place from reinforcements first
            if other_player.reinforcements > 0:
                system.place_command_token(other_player.id)
                # Consume the token from reinforcements
                other_player.consume_reinforcement()
            else:
                # Rule 32.2.a: If no reinforcements, place from command sheet
                # Check if player has any command tokens on their command sheet
                total_command_tokens = other_player.command_sheet.get_total_tokens()
                if total_command_tokens > 0:
                    system.place_command_token(other_player.id)
                    # Remove a token from the command sheet (prefer tactic, then fleet, then strategy)
                    other_player.command_sheet.consume_any_token()
                # If no tokens available anywhere, the player simply doesn't place a token

        # Ready up to 2 exhausted planets controlled by the player
        planets_to_ready = kwargs.get("planets_to_ready", [])
        if len(planets_to_ready) > 2:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Cannot ready more than 2 planets with Diplomacy primary ability",
            )

        # Get all exhausted planets controlled by the player
        all_exhausted_planets = []
        if game_state.galaxy:
            all_exhausted_planets = (
                game_state.galaxy.find_exhausted_planets_controlled_by_player(player_id)
            )

        # If no specific planets specified, ready up to 2 exhausted planets automatically
        if not planets_to_ready:
            all_exhausted_planets.sort(key=lambda p: p.name)
            planets_to_ready = [p.name for p in all_exhausted_planets[:2]]

        # Validate and ready the specified planets
        readied_planets = []
        for planet_name in planets_to_ready:
            # Find the planet using Galaxy helper method
            target_planet = None
            if game_state.galaxy:
                target_planet = game_state.galaxy.find_planet_by_name(
                    planet_name, player_id
                )

            if not target_planet:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Planet {planet_name} not found or not controlled by player {player_id}",
                )

            if not target_planet.is_exhausted():
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Planet {planet_name} is not exhausted",
                )

            target_planet.ready()
            readied_planets.append(planet_name)

        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message=None,
            additional_data={"readied_planets": readied_planets},
        )

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Diplomacy strategy card.

        LRR 32.3: After the active player resolves the primary ability of the
        "Diplomacy" strategy card, each other player, beginning with the player
        to the left of the active player and proceeding clockwise, may spend one
        command token from their strategy pool to ready up to two exhausted
        planets they control.

        Args:
            player_id: The player executing the secondary ability
            game_state: Game state for full integration
            **kwargs: Additional parameters - expects 'planet_ids' list

        Returns:
            Result of the secondary ability execution
        """
        if not game_state:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Game state is required for Diplomacy secondary ability",
            )

        # Find the player
        player = None
        for player_obj in game_state.players:
            if player_obj.id == player_id:
                player = player_obj
                break

        if not player:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} not found in game state",
            )

        # Check if player has command tokens in strategy pool
        if player.command_sheet.strategy_pool <= 0:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} has no command tokens in strategy pool",
            )

        planet_ids = kwargs.get("planet_ids", [])
        if not planet_ids:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Planet IDs must be provided for Diplomacy secondary ability",
            )

        # Rule 32.3: Can ready up to 2 planets
        if len(planet_ids) > 2:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Diplomacy secondary ability can ready at most 2 planets",
            )

        # Find and validate planets
        planets_to_ready = []
        for planet_id in planet_ids:
            found_planet = None
            # Search through all systems for the planet
            if game_state.galaxy:
                for system in game_state.galaxy.system_objects.values():
                    for planet_obj in system.planets:
                        if planet_obj.name == planet_id:
                            found_planet = planet_obj
                            break
                    if found_planet:
                        break

            if not found_planet:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Planet {planet_id} not found",
                )

            # Check if player controls the planet
            if found_planet.controlled_by != player_id:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Player {player_id} does not control planet {planet_id}",
                )

            # Rule 32.3: Can only ready exhausted planets
            if not found_planet.is_exhausted():
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Planet {planet_id} is not exhausted and cannot be readied",
                )

            planets_to_ready.append(found_planet)

        # Spend command token from strategy pool before mutating state
        if not player.command_sheet.spend_strategy_token():
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Failed to spend strategy token for player {player_id}",
            )

        # Ready the planets
        for planet in planets_to_ready:
            planet.ready()

        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message=None,
        )
