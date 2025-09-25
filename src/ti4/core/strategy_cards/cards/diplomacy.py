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
            **kwargs: Additional parameters - expects 'system_id' for the chosen system;
                     optionally 'planets_to_ready' (alias: 'planet_ids') with up to two planet names to ready

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
        if not any(p.controlled_by == player_id for p in system.planets):
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} does not control any planet in system {system_id}",
            )

        # Ready up to 2 exhausted planets controlled by the player
        planets_to_ready = kwargs.get("planets_to_ready", kwargs.get("planet_ids", []))
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

        # VALIDATION PHASE: Validate all planets before any mutations
        planets_to_ready_objs = []
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

            planets_to_ready_objs.append(target_planet)

        # MUTATION PHASE: All validations passed, now perform mutations
        # Rule 32.2: Each other player places one command token from their reinforcements in that system
        other_players = [p for p in game_state.players if p.id != player_id]
        for other_player in other_players:
            # Rule 32.2.b: If player already has a command token in the system, don't place another
            if system.has_command_token(other_player.id):
                continue

            # Try to consume from reinforcements first; place only after successful spend
            if other_player.consume_reinforcement():
                system.place_command_token(other_player.id)
            else:
                # Rule 32.2.a: If no reinforcements, take from command sheet (prefer tactic > fleet > strategy)
                consumed_pool = other_player.command_sheet.consume_any_token()
                if consumed_pool is not None:
                    system.place_command_token(other_player.id)
                # If no tokens available anywhere, the player simply doesn't place a token

        # Ready the validated planets
        readied_planets = []
        for target_planet in planets_to_ready_objs:
            target_planet.ready()
            readied_planets.append(target_planet.name)

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
            **kwargs: Additional parameters - expects 'planet_ids' list (alias: 'planets_to_ready')

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

        planet_ids = kwargs.get("planet_ids", kwargs.get("planets_to_ready", []))
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

        # Find and validate ALL planets before any state mutation
        planets_to_ready = []
        for planet_id in planet_ids:
            found_planet = None
            if game_state.galaxy:
                found_planet = game_state.galaxy.find_planet_by_name(
                    planet_id, player_id
                )

            if not found_planet:
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

        # All validations passed - now perform state mutations
        # Spend command token from strategy pool
        if not player.command_sheet.spend_strategy_token():
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} has no command tokens in strategy pool",
            )

        # Ready the planets
        for planet in planets_to_ready:
            planet.ready()

        return StrategyCardAbilityResult(
            success=True,
            player_id=player_id,
            error_message=None,
            command_tokens_spent=1,
        )
