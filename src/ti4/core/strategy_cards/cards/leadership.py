"""Leadership Strategy Card implementation for TI4.

This module implements the Leadership strategy card following the
BaseStrategyCard pattern established for all strategy cards.

LRR Reference: Rule 52 - STRATEGY CARD (Leadership)
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Optional

from ..base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult
from ..strategic_action import StrategyCardType

if TYPE_CHECKING:
    from ...game_state import GameState
    from ...resource_management import ResourceManager


class LeadershipStrategyCard(BaseStrategyCard):
    """Leadership Strategy Card implementation.

    LRR Reference: Rule 52 - The "Leadership" strategy card.

    This card allows the active player to gain command tokens and spend influence
    for additional tokens. Other players can participate by spending influence.
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

        LRR Reference: Rule 52 - Leadership has initiative value "1"
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
            **kwargs: Additional parameters including:
                - player: Player object (required)
                - token_distribution: Dict specifying token allocation (required)
                - planets_to_exhaust: List of planet names (backward compatibility)
                - trade_goods_to_spend: Number of trade goods (backward compatibility)
                - resource_manager: ResourceManager instance (new interface)
                - influence_to_spend: Amount of influence to spend (new interface)

        Returns:
            Result of the primary ability execution
        """
        # Extract required parameters
        player = kwargs.get("player")
        token_distribution = kwargs.get("token_distribution", {})

        # Support both old and new interfaces
        resource_manager = kwargs.get("resource_manager")
        influence_to_spend = kwargs.get("influence_to_spend")

        # Backward compatibility parameters
        planets_to_exhaust = kwargs.get("planets_to_exhaust", [])
        trade_goods_to_spend = kwargs.get("trade_goods_to_spend", 0)

        if player is None and game_state is not None:
            # Derive the player from game_state if not provided
            player = next((p for p in game_state.players if p.id == player_id), None)
        if player is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Player parameter is required for Leadership primary ability",
            )
        if getattr(player, "id", None) != player_id:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="player.id does not match player_id",
            )

        try:
            # Rule 52.2: Gain 3 base command tokens
            base_tokens = 3

            # Handle influence spending - support both new and old interfaces
            influence_result = self._handle_influence_spending(
                player_id,
                player,
                game_state,
                resource_manager,
                influence_to_spend,
                planets_to_exhaust,
                trade_goods_to_spend,
            )
            if not influence_result["success"]:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=influence_result["error_message"],
                )

            total_influence = influence_result["total_influence"]

            # Calculate tokens: 3 base + 1 per 3 influence spent
            reinforcements = player.reinforcements
            max_base_tokens = min(base_tokens, reinforcements)
            additional_tokens = min(
                total_influence // 3, reinforcements - max_base_tokens
            )
            total_tokens_needed = max_base_tokens + additional_tokens

            # Validate token_distribution BEFORE any state mutations
            valid_pools = {"tactic", "fleet", "strategy"}
            if any(
                (k not in valid_pools) or (int(v) < 0)
                for k, v in token_distribution.items()
            ):
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message="Invalid token_distribution; allowed keys: tactic, fleet, strategy; counts must be >= 0.",
                )

            # Check if player is requesting more tokens than they can get
            requested_tokens = sum(int(v) for v in token_distribution.values())
            if requested_tokens > total_tokens_needed:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Insufficient influence: requested {requested_tokens} tokens but can only gain {total_tokens_needed} tokens ({max_base_tokens} base + {additional_tokens} from influence)",
                )

            if requested_tokens < total_tokens_needed:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"token_distribution must allocate exactly {total_tokens_needed} tokens.",
                )

            # All validation passed - now perform state mutations
            # Note: If using ResourceManager, spending was already executed above
            if resource_manager is None or influence_to_spend is None:
                # Only execute old interface spending if not using ResourceManager
                if trade_goods_to_spend > 0:
                    if not player.spend_trade_goods(trade_goods_to_spend):
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message=f"Failed to spend {trade_goods_to_spend} trade goods",
                        )
                if planets_to_exhaust:
                    if game_state is None:
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message="game_state is required to exhaust planets",
                        )
                    self._exhaust_planets(planets_to_exhaust, game_state, player_id)

            # Distribute tokens using Player.gain_command_token
            tokens_distributed = 0
            for pool_name, count in token_distribution.items():
                for _ in range(
                    min(int(count), total_tokens_needed - tokens_distributed)
                ):
                    success = player.gain_command_token(pool_name)
                    if not success:
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message="Reinforcement limit reached while placing tokens.",
                        )
                    tokens_distributed += 1
                    if tokens_distributed >= total_tokens_needed:
                        break

            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                additional_data={
                    "base_tokens_gained": max_base_tokens,
                    "influence_tokens_gained": additional_tokens,
                    "total_tokens_gained": tokens_distributed,
                    "influence_spent": total_influence,
                    "trade_goods_spent": trade_goods_to_spend,
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
            **kwargs: Additional parameters (player, token_distribution, planets_to_exhaust, trade_goods_to_spend, participate)

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

        # Support both old and new interfaces
        resource_manager = kwargs.get("resource_manager")
        influence_to_spend = kwargs.get("influence_to_spend")

        # Backward compatibility parameters
        planets_to_exhaust = kwargs.get("planets_to_exhaust", [])
        trade_goods_to_spend = kwargs.get("trade_goods_to_spend", 0)

        if player is None and game_state is not None:
            player = next((p for p in game_state.players if p.id == player_id), None)
        if player is None:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="Player parameter is required for Leadership secondary ability",
            )
        if getattr(player, "id", None) != player_id:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message="player.id does not match player_id",
            )

        try:
            # Rule 52.3: Only influence conversion, no base tokens
            # Rule 20.5a: Leadership secondary ability doesn't cost command token

            # Handle influence spending - support both new and old interfaces
            influence_result = self._handle_influence_spending(
                player_id,
                player,
                game_state,
                resource_manager,
                influence_to_spend,
                planets_to_exhaust,
                trade_goods_to_spend,
            )
            if not influence_result["success"]:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=influence_result["error_message"],
                )

            total_influence = influence_result["total_influence"]

            # Calculate tokens from influence (1 per 3 influence)
            reinforcements = player.reinforcements
            tokens_from_influence = min(total_influence // 3, reinforcements)

            # Validate token_distribution BEFORE any state mutations
            valid_pools = {"tactic", "fleet", "strategy"}
            if any(
                (k not in valid_pools) or (int(v) < 0)
                for k, v in token_distribution.items()
            ):
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message="Invalid token_distribution; allowed keys: tactic, fleet, strategy; counts must be >= 0.",
                )

            # Check if player is requesting more tokens than they can get
            requested_tokens = sum(int(v) for v in token_distribution.values())
            if requested_tokens > tokens_from_influence:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"Insufficient influence: requested {requested_tokens} tokens but can only gain {tokens_from_influence} tokens from influence",
                )

            if requested_tokens < tokens_from_influence:
                return StrategyCardAbilityResult(
                    success=False,
                    player_id=player_id,
                    error_message=f"token_distribution must allocate exactly {tokens_from_influence} tokens.",
                )

            # All validation passed - now perform state mutations
            # Note: If using ResourceManager, spending was already executed above
            if resource_manager is None or influence_to_spend is None:
                # Only execute old interface spending if not using ResourceManager
                if trade_goods_to_spend > 0:
                    if not player.spend_trade_goods(trade_goods_to_spend):
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message=f"Failed to spend {trade_goods_to_spend} trade goods",
                        )
                if planets_to_exhaust:
                    if game_state is None:
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message="game_state is required to exhaust planets",
                        )
                    self._exhaust_planets(planets_to_exhaust, game_state, player_id)

            # Distribute tokens using Player.gain_command_token
            tokens_distributed = 0
            for pool_name, count in token_distribution.items():
                for _ in range(
                    min(int(count), tokens_from_influence - tokens_distributed)
                ):
                    success = player.gain_command_token(pool_name)
                    if not success:
                        return StrategyCardAbilityResult(
                            success=False,
                            player_id=player_id,
                            error_message="Reinforcement limit reached while placing tokens.",
                        )
                    tokens_distributed += 1
                    if tokens_distributed >= tokens_from_influence:
                        break

            return StrategyCardAbilityResult(
                success=True,
                player_id=player_id,
                additional_data={
                    "tokens_gained": tokens_distributed,
                    "influence_spent": total_influence,
                    "trade_goods_spent": trade_goods_to_spend,
                    "participated": True,
                },
            )

        except Exception as e:
            return StrategyCardAbilityResult(
                success=False,
                player_id=player_id,
                error_message=f"Error executing Leadership secondary ability: {str(e)}",
            )

    def _validate_planets_for_exhaustion(
        self, planets_to_exhaust: Sequence[str], game_state: "GameState", player: Any
    ) -> dict[str, Any]:
        """Validate that the player can exhaust the specified planets for influence.

        Args:
            planets_to_exhaust: List of planet names to exhaust
            game_state: Game state to get player's planets
            player: The player attempting to exhaust planets

        Returns:
            dict with 'valid' (bool), 'total_influence' (int), and 'error' (str) keys
        """
        if not planets_to_exhaust:
            return {"valid": True, "total_influence": 0, "error": ""}

        # Get player's controlled planets from game state
        controlled_planets_list = game_state.get_player_planets(player.id)
        controlled_planets = {p.name: p for p in controlled_planets_list}

        total_influence = 0
        seen: set[str] = set()
        for planet_name in planets_to_exhaust:
            if planet_name in seen:
                return {
                    "valid": False,
                    "total_influence": 0,
                    "error": f"Planet '{planet_name}' listed multiple times",
                }
            seen.add(planet_name)

            # Check if planet is controlled by player
            if planet_name not in controlled_planets:
                return {
                    "valid": False,
                    "total_influence": 0,
                    "error": f"Player does not control planet '{planet_name}'",
                }

            planet = controlled_planets[planet_name]
            if planet.is_exhausted():
                return {
                    "valid": False,
                    "total_influence": 0,
                    "error": f"Planet '{planet_name}' is already exhausted",
                }

            # Prefer method accessor if available, fallback to attribute for mocks
            influence_value = None
            if hasattr(planet, "get_influence"):
                influence_value = planet.get_influence()
            elif hasattr(planet, "influence"):
                influence_value = getattr(planet, "influence", None)

            if influence_value is None:
                return {
                    "valid": False,
                    "total_influence": 0,
                    "error": f"Planet '{planet_name}' has no influence value",
                }

            # Convert to integer
            try:
                influence_int = int(influence_value)
                if influence_int < 0:
                    return {
                        "valid": False,
                        "total_influence": 0,
                        "error": f"Planet '{planet_name}' cannot have negative influence",
                    }
            except (ValueError, TypeError):
                return {
                    "valid": False,
                    "total_influence": 0,
                    "error": f"Planet '{planet_name}' has invalid influence value",
                }

            total_influence += influence_int

        return {"valid": True, "total_influence": total_influence, "error": ""}

    def _handle_influence_spending(
        self,
        player_id: str,
        player: Any,
        game_state: Optional["GameState"],
        resource_manager: Optional["ResourceManager"],
        influence_to_spend: Optional[int],
        planets_to_exhaust: list[str],
        trade_goods_to_spend: int,
    ) -> dict[str, Any]:
        """Handle influence spending using either new ResourceManager or old interface.

        Args:
            player_id: The player ID
            player: The player object
            game_state: Optional game state
            resource_manager: Optional ResourceManager instance
            influence_to_spend: Amount of influence to spend (new interface)
            planets_to_exhaust: List of planet names (old interface)
            trade_goods_to_spend: Number of trade goods (old interface)

        Returns:
            Dict with success, total_influence, spending_result, and error_message keys
        """
        if resource_manager is not None and influence_to_spend is not None:
            # New interface: use ResourceManager for influence validation and spending
            if not resource_manager.can_afford_spending(
                player_id, influence_amount=influence_to_spend, for_voting=False
            ):
                available_influence = resource_manager.calculate_available_influence(
                    player_id, for_voting=False
                )
                return {
                    "success": False,
                    "error_message": f"Insufficient influence: need {influence_to_spend}, have {available_influence}",
                    "total_influence": 0,
                    "spending_result": None,
                }

            # Create and execute spending plan
            spending_plan = resource_manager.create_spending_plan(
                player_id, influence_amount=influence_to_spend, for_voting=False
            )
            if not spending_plan.is_valid:
                return {
                    "success": False,
                    "error_message": spending_plan.error_message
                    or "Invalid spending plan",
                    "total_influence": 0,
                    "spending_result": None,
                }

            spending_result = resource_manager.execute_spending_plan(spending_plan)
            if not spending_result.success:
                return {
                    "success": False,
                    "error_message": spending_result.error_message
                    or "Failed to execute spending plan",
                    "total_influence": 0,
                    "spending_result": None,
                }

            return {
                "success": True,
                "total_influence": influence_to_spend,
                "spending_result": spending_result,
                "error_message": None,
            }

        else:
            # Backward compatibility: use old planet exhaustion interface
            total_influence = 0

            if planets_to_exhaust and game_state:
                validation_result = self._validate_planets_for_exhaustion(
                    planets_to_exhaust, game_state, player
                )
                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error_message": validation_result["error"],
                        "total_influence": 0,
                        "spending_result": None,
                    }
                total_influence = validation_result["total_influence"]

            # Add trade goods to influence total (1 trade good = 1 influence)
            trade_goods_to_spend = max(0, int(trade_goods_to_spend))
            if trade_goods_to_spend > player.get_trade_goods():
                return {
                    "success": False,
                    "error_message": f"Insufficient trade goods: cannot spend {trade_goods_to_spend}, player only has {player.get_trade_goods()}",
                    "total_influence": 0,
                    "spending_result": None,
                }

            total_influence += trade_goods_to_spend

            return {
                "success": True,
                "total_influence": total_influence,
                "spending_result": None,
                "error_message": None,
            }

    def _exhaust_planets(
        self, planets_to_exhaust: list[str], game_state: "GameState", player_id: str
    ) -> None:
        """Exhaust the specified planets.

        Args:
            planets_to_exhaust: List of planet names to exhaust
            game_state: Game state to get planets
            player_id: Player ID to filter planets by ownership
        """
        if game_state.galaxy is None:
            raise ValueError("Galaxy is not available; cannot exhaust planets.")

        for planet_name in planets_to_exhaust:
            # Find the planet using Galaxy helper method with player filter and exhaust it
            planet = game_state.galaxy.find_planet_by_name(planet_name, player_id)
            if planet is None:
                raise ValueError(
                    f"Planet '{planet_name}' not found or not controlled by player '{player_id}'."
                )
            planet.exhaust()
