"""Leadership Strategy Card implementation for TI4.

This module implements the Leadership strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 83 - STRATEGY CARD (Leadership)
"""

from typing import TYPE_CHECKING, Any, Optional

from ..base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from ..strategic_action import StrategyCardType

if TYPE_CHECKING:
    from ...game_state import GameState


class LeadershipStrategyCard(BaseStrategyCard):
    """Implementation of the Leadership strategy card.

    LRR Reference: Rule 83 - The "Leadership" strategy card.
    This card's initiative value is "1."
    """

    def __init__(self) -> None:
        """Initialize the Leadership strategy card."""
        pass

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.LEADERSHIP
        """
        return StrategyCardType.LEADERSHIP

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Leadership strategy card.

        Returns:
            The initiative value (1)

        LRR Reference: Rule 83 - Leadership has initiative value "1"
        """
        return 1

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Leadership strategy card.

        LRR 52.2: "the active player gains three command tokens. Then, that player
        can spend any amount of their influence to gain one command token for every
        three influence they spend."

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters (player, token_distribution, influence_to_spend)

        Returns:
            Result of the primary ability execution
        """
        # Extract required parameters
        player = kwargs.get("player")
        token_distribution = kwargs.get("token_distribution", {})
        influence_to_spend = kwargs.get("influence_to_spend", 0)

        if player is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Player parameter is required for Leadership primary ability",
            )

        try:
            # Rule 52.2: Gain 3 base command tokens
            base_tokens = 3

            # Calculate additional tokens from influence (3:1 ratio)
            additional_tokens = influence_to_spend // 3
            total_tokens = base_tokens + additional_tokens

            # Validate we have enough reinforcements
            if player.reinforcements < total_tokens:
                # Rule 20.3a: Cannot gain tokens if none available in reinforcements
                total_tokens = player.reinforcements

            # Distribute tokens to pools as specified
            tokens_distributed = 0
            for pool_name, count in token_distribution.items():
                if tokens_distributed + count > total_tokens:
                    count = total_tokens - tokens_distributed

                if count > 0:
                    if pool_name == "tactic":
                        object.__setattr__(
                            player.command_sheet,
                            "tactic_pool",
                            player.command_sheet.tactic_pool + count,
                        )
                    elif pool_name == "fleet":
                        object.__setattr__(
                            player.command_sheet,
                            "fleet_pool",
                            player.command_sheet.fleet_pool + count,
                        )
                    elif pool_name == "strategy":
                        object.__setattr__(
                            player.command_sheet,
                            "strategy_pool",
                            player.command_sheet.strategy_pool + count,
                        )

                    tokens_distributed += count

                if tokens_distributed >= total_tokens:
                    break

            # Update reinforcements
            object.__setattr__(
                player, "reinforcements", player.reinforcements - tokens_distributed
            )

            # Handle influence spending if any
            if influence_to_spend > 0 and game_state:
                self._spend_influence(player, influence_to_spend, game_state)

            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                additional_data={
                    "base_tokens_gained": base_tokens,
                    "influence_tokens_gained": additional_tokens,
                    "total_tokens_gained": tokens_distributed,
                    "influence_spent": influence_to_spend,
                },
            )

        except Exception as e:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Error executing Leadership primary ability: {str(e)}",
            )

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Leadership strategy card.

        LRR 52.3: "each other player, beginning with the player to the left of the
        active player and proceeding clockwise, may spend any amount of influence
        to gain one command token for every three influence they spend."

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters (player, token_distribution, influence_to_spend, participate)

        Returns:
            Result of the secondary ability execution
        """
        # Check if player chooses to participate
        participate = kwargs.get("participate", True)
        if not participate:
            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                additional_data={"participated": False},
            )

        # Extract required parameters
        player = kwargs.get("player")
        token_distribution = kwargs.get("token_distribution", {})
        influence_to_spend = kwargs.get("influence_to_spend", 0)

        if player is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Player parameter is required for Leadership secondary ability",
            )

        try:
            # Rule 52.3: Only influence conversion, no base tokens
            # Rule 20.5a: Leadership secondary ability doesn't cost command token

            # Calculate tokens from influence (3:1 ratio)
            tokens_from_influence = influence_to_spend // 3

            # Validate we have enough reinforcements
            if player.reinforcements < tokens_from_influence:
                # Rule 20.3a: Cannot gain tokens if none available in reinforcements
                tokens_from_influence = player.reinforcements

            # Distribute tokens to pools as specified
            tokens_distributed = 0
            for pool_name, count in token_distribution.items():
                if tokens_distributed + count > tokens_from_influence:
                    count = tokens_from_influence - tokens_distributed

                if count > 0:
                    if pool_name == "tactic":
                        object.__setattr__(
                            player.command_sheet,
                            "tactic_pool",
                            player.command_sheet.tactic_pool + count,
                        )
                    elif pool_name == "fleet":
                        object.__setattr__(
                            player.command_sheet,
                            "fleet_pool",
                            player.command_sheet.fleet_pool + count,
                        )
                    elif pool_name == "strategy":
                        object.__setattr__(
                            player.command_sheet,
                            "strategy_pool",
                            player.command_sheet.strategy_pool + count,
                        )

                    tokens_distributed += count

                if tokens_distributed >= tokens_from_influence:
                    break

            # Update reinforcements
            if tokens_distributed > 0:
                object.__setattr__(
                    player, "reinforcements", player.reinforcements - tokens_distributed
                )

            # Handle influence spending if any
            if influence_to_spend > 0 and game_state:
                self._spend_influence(player, influence_to_spend, game_state)

            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                additional_data={
                    "tokens_gained": tokens_distributed,
                    "influence_spent": influence_to_spend,
                    "participated": True,
                },
            )

        except Exception as e:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Error executing Leadership secondary ability: {str(e)}",
            )

    def _spend_influence(
        self, player: Any, influence_to_spend: int, game_state: "GameState"
    ) -> None:
        """Helper method to spend influence by exhausting planets.

        Args:
            player: The player spending influence
            influence_to_spend: Amount of influence to spend
            game_state: Game state to get player's planets
        """
        if influence_to_spend <= 0:
            return

        # Get player's controlled planets from game state
        controlled_planets = game_state.get_player_planets(player.id)

        remaining_influence = influence_to_spend
        for planet in controlled_planets:
            if remaining_influence <= 0:
                break

            if not planet.is_exhausted() and planet.influence > 0:
                # Exhaust this planet
                planet.exhaust()
                remaining_influence -= planet.influence
