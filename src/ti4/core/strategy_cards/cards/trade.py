"""Trade Strategy Card implementation for TI4.

This module implements the Trade strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 83 - STRATEGY CARD (Trade)
"""

import time
from typing import TYPE_CHECKING, Any, Optional

from ..base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from ..strategic_action import StrategyCardType

if TYPE_CHECKING:
    from ...game_state import GameState


class TradeStrategyCard(BaseStrategyCard):
    """Implementation of the Trade strategy card.

    LRR Reference: Rule 83 - The "Trade" strategy card.
    This card's initiative value is "5."
    """

    def __init__(self) -> None:
        """Initialize the Trade strategy card."""
        # Track chosen players per game state for multi-player support
        self._chosen_players_by_game: dict[int, list[str]] = {}

        # Performance monitoring
        self._performance_metrics: dict[str, list[float]] = {
            "primary_ability_times": [],
            "secondary_ability_times": [],
        }

    def get_card_type(self) -> StrategyCardType:
        """Get the strategy card type.

        Returns:
            StrategyCardType.TRADE
        """
        return StrategyCardType.TRADE

    def get_initiative_value(self) -> int:
        """Get the initiative value of the Trade strategy card.

        Returns:
            The initiative value (5)

        LRR Reference: Rule 83 - Trade has initiative value "5"
        """
        return 5

    def execute_primary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the primary ability of the Trade strategy card.

        This method orchestrates all three steps of the Trade primary ability:
        1. Gain 3 trade goods
        2. Replenish commodities to faction maximum
        3. Choose players for free secondary ability

        Includes comprehensive error handling and rollback capability to ensure
        game state consistency if any step fails.

        Args:
            player_id: The active player executing the primary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card
                chosen_players: Optional list of player IDs to grant free secondary ability access

        Returns:
            Result of the primary ability execution

        Requirements: 6.1, 6.2, 9.2, 9.3 - Complete workflow execution with error handling and rollback

        LRR Reference: Rule 92 - Trade primary ability
        Step 1: Gain 3 trade goods
        Step 2: Replenish commodities to faction maximum
        Step 3: Choose players for free secondary ability
        """
        # Performance monitoring - start timing
        start_time = time.perf_counter()
        if game_state is None:
            # Placeholder implementation - specific abilities need user confirmation
            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                error_message="Trade primary ability implementation requires user confirmation of specific effects",
            )

        from ...exceptions import TI4GameError

        # Capture initial state for rollback capability
        player = game_state.get_player(player_id)
        if player is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Player {player_id} not found in game state",
            )

        initial_trade_goods = player.get_trade_goods()
        initial_commodities = player.get_commodities()

        try:
            # Step 1: Gain 3 trade goods
            self._gain_trade_goods(player_id, game_state)

            # Step 2: Replenish commodities to faction maximum
            self._replenish_commodities(player_id, game_state)

            # Step 3: Choose players for free secondary ability (if provided)
            chosen_players = kwargs.get("chosen_players")
            if chosen_players is not None:
                self._process_chosen_players(player_id, chosen_players, game_state)

            # All steps completed successfully
            result = StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
            )

            # Performance monitoring - record execution time
            execution_time = (
                time.perf_counter() - start_time
            ) * 1000  # Convert to milliseconds
            self._performance_metrics["primary_ability_times"].append(execution_time)

            return result

        except TI4GameError as e:
            # Rollback changes if any step failed
            self._rollback_primary_ability_changes(
                player_id, game_state, initial_trade_goods, initial_commodities
            )

            # Performance monitoring - record execution time even for errors
            execution_time = (time.perf_counter() - start_time) * 1000
            self._performance_metrics["primary_ability_times"].append(execution_time)

            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=str(e),
            )

        except Exception as e:
            # Handle unexpected errors with rollback
            self._rollback_primary_ability_changes(
                player_id, game_state, initial_trade_goods, initial_commodities
            )

            # Performance monitoring - record execution time even for errors
            execution_time = (time.perf_counter() - start_time) * 1000
            self._performance_metrics["primary_ability_times"].append(execution_time)

            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Unexpected error during Trade primary ability: {str(e)}",
            )

    def _gain_trade_goods(self, player_id: str, game_state: "GameState") -> None:
        """Gain 3 trade goods for the active player.

        Args:
            player_id: The player gaining trade goods
            game_state: Current game state (modified in place)

        Raises:
            TI4GameError: If player not found in game state

        Requirements: 2.1, 2.2, 2.3, 7.1 - Trade goods gain with resource management integration
        """
        from ...exceptions import TI4GameError

        # Validate player exists
        player = game_state.get_player(player_id)
        if player is None:
            raise TI4GameError(f"Player {player_id} not found in game state")

        # Optimized: Gain 3 trade goods in a single operation for better performance
        player.gain_trade_goods(3)

    def _replenish_commodities(self, player_id: str, game_state: "GameState") -> None:
        """Replenish commodities to faction maximum for the active player.

        Args:
            player_id: The player replenishing commodities
            game_state: Current game state (modified in place)

        Raises:
            TI4GameError: If player not found in game state

        Requirements: 3.1, 3.2, 3.3, 7.2 - Commodity replenishment with faction limit integration
        """
        from ...exceptions import TI4GameError

        # Validate player exists
        player = game_state.get_player(player_id)
        if player is None:
            raise TI4GameError(f"Player {player_id} not found in game state")

        # Optimized: Replenish commodities to faction maximum in a single operation
        player.replenish_commodities()

    def _process_chosen_players(
        self, active_player_id: str, chosen_players: list[str], game_state: "GameState"
    ) -> None:
        """Process the list of chosen players for free secondary ability access.

        Args:
            active_player_id: The player executing the primary ability (cannot choose themselves)
            chosen_players: List of player IDs chosen for free secondary ability
            game_state: Current game state (modified in place)

        Raises:
            TI4GameError: If invalid player IDs are provided or active player tries to choose themselves

        Requirements: 4.1, 4.2, 4.3, 8.1, 9.1 - Player selection mechanism with validation
        """
        from ...exceptions import TI4GameError

        # Handle duplicates by converting to set and back to list
        unique_chosen_players = list(set(chosen_players))

        # Validate each chosen player
        for player_id in unique_chosen_players:
            # Validate player exists in game state
            player = game_state.get_player(player_id)
            if player is None:
                raise TI4GameError(f"Invalid player ID: {player_id}")

            # Validate player is not choosing themselves
            if player_id == active_player_id:
                raise TI4GameError(
                    "Active player cannot choose themselves for free secondary ability"
                )

        # Store chosen players for this game state
        game_id = id(game_state)
        self._chosen_players_by_game[game_id] = unique_chosen_players

    def _rollback_primary_ability_changes(
        self,
        player_id: str,
        game_state: "GameState",
        initial_trade_goods: int,
        initial_commodities: int,
    ) -> None:
        """Rollback changes made during primary ability execution.

        This method restores the player's resources to their initial state
        if any step of the primary ability fails, ensuring game state consistency.

        Args:
            player_id: The player whose resources need to be rolled back
            game_state: Current game state (modified in place)
            initial_trade_goods: Trade goods count before primary ability execution
            initial_commodities: Commodity count before primary ability execution

        Requirements: 9.3 - Rollback capability for failed operations
        """
        player = game_state.get_player(player_id)
        if player is not None:
            # Restore trade goods to initial amount
            current_trade_goods = player.get_trade_goods()
            if current_trade_goods != initial_trade_goods:
                trade_goods_diff = current_trade_goods - initial_trade_goods
                if trade_goods_diff > 0:
                    # Remove excess trade goods
                    player.spend_trade_goods(trade_goods_diff)
                elif trade_goods_diff < 0:
                    # Add missing trade goods
                    player.gain_trade_goods(-trade_goods_diff)

            # Restore commodities to initial amount
            current_commodities = player.get_commodities()
            if current_commodities != initial_commodities:
                commodity_diff = current_commodities - initial_commodities
                if commodity_diff > 0:
                    # Remove excess commodities
                    player.spend_commodities(commodity_diff)
                elif commodity_diff < 0:
                    # Add missing commodities
                    player.add_commodities(-commodity_diff)

    def execute_secondary_ability(
        self,
        player_id: str,
        game_state: Optional["GameState"] = None,
        **kwargs: Any,
    ) -> StrategyCardAbilityResult:
        """Execute the secondary ability of the Trade strategy card.

        LRR Reference: Rule 92 - Trade secondary ability
        Non-active players may spend 1 command token from their strategy pool
        to replenish commodities to their faction maximum.

        Args:
            player_id: The player executing the secondary ability
            game_state: Optional game state for full integration
            **kwargs: Additional parameters specific to the card
                is_free: Boolean indicating if this execution is free (chosen by active player)

        Returns:
            Result of the secondary ability execution

        Requirements: 5.1, 5.2, 5.3, 5.4, 7.3 - Command token validation and commodity replenishment
        """
        # Performance monitoring - start timing
        start_time = time.perf_counter()
        if game_state is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Game state is required for Trade secondary ability execution",
            )

        from ...exceptions import TI4GameError

        try:
            # Check if execution is free (player was chosen by active player or explicitly set)
            is_free = kwargs.get("is_free", False)

            # Auto-detect if player was chosen for free execution
            if not is_free:
                chosen_players = self.get_chosen_players(game_state)
                is_free = player_id in chosen_players

            # Validate player exists
            player = game_state.get_player(player_id)
            if player is None:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Player {player_id} not found in game state",
                )

            # Step 1: Spend command token (unless execution is free)
            if not is_free:
                # Check if player has command tokens in strategy pool
                if not player.command_sheet.has_strategy_tokens():
                    return StrategyCardAbilityResult(
                        success=False,
                        player_id=player_id,
                        error_message="Insufficient command tokens in strategy pool",
                    )

                # Spend the command token
                success = player.command_sheet.spend_strategy_token()
                if not success:
                    return StrategyCardAbilityResult(
                        success=False,
                        player_id=player_id,
                        error_message="Failed to spend command token from strategy pool",
                    )

            # Step 2: Replenish commodities to faction maximum
            player.replenish_commodities()

            # Performance monitoring - record execution time
            execution_time = (
                time.perf_counter() - start_time
            ) * 1000  # Convert to milliseconds
            self._performance_metrics["secondary_ability_times"].append(execution_time)

            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
            )

        except TI4GameError as e:
            # Performance monitoring - record execution time even for errors
            execution_time = (time.perf_counter() - start_time) * 1000
            self._performance_metrics["secondary_ability_times"].append(execution_time)

            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=str(e),
            )

        except Exception as e:
            # Performance monitoring - record execution time even for errors
            execution_time = (time.perf_counter() - start_time) * 1000
            self._performance_metrics["secondary_ability_times"].append(execution_time)

            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Unexpected error during Trade secondary ability: {str(e)}",
            )

    def get_chosen_players(self, game_state: "GameState") -> list[str]:
        """Get the list of players chosen for free secondary ability execution.

        Args:
            game_state: Current game state

        Returns:
            List of player IDs chosen for free secondary ability access

        Requirements: 8.2 - Chosen player tracking per execution
        """
        game_id = id(game_state)
        return self._chosen_players_by_game.get(game_id, [])

    def get_performance_metrics(self) -> dict[str, dict[str, float]]:
        """Get performance metrics for the Trade strategy card.

        Returns:
            Dictionary containing performance statistics for primary and secondary abilities

        Requirements: 11.3 - Performance benchmarking and monitoring
        """
        metrics = {}

        for ability_type, times in self._performance_metrics.items():
            if times:
                metrics[ability_type] = {
                    "count": len(times),
                    "average_ms": sum(times) / len(times),
                    "min_ms": min(times),
                    "max_ms": max(times),
                    "total_ms": sum(times),
                }
            else:
                metrics[ability_type] = {
                    "count": 0,
                    "average_ms": 0.0,
                    "min_ms": 0.0,
                    "max_ms": 0.0,
                    "total_ms": 0.0,
                }

        return metrics

    def reset_performance_metrics(self) -> None:
        """Reset performance metrics for the Trade strategy card.

        This method clears all collected performance data, useful for
        starting fresh measurements or preventing memory growth over time.

        Requirements: 11.3 - Performance benchmarking and monitoring
        """
        self._performance_metrics = {
            "primary_ability_times": [],
            "secondary_ability_times": [],
        }
