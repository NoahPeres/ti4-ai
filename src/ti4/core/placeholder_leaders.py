"""Placeholder leader implementations for testing architecture validation.

This module contains placeholder leader implementations with different ability patterns
to validate the leader system architecture. These are NOT actual TI4 leaders but
serve as examples for testing different complexity levels.

LRR References:
- Rule 51: LEADERS
- Requirements 7.1, 7.2, 7.3, 7.4, 7.5

Note: These are placeholder implementations for architecture testing only.
Actual faction leaders must be implemented based on official TI4 compendium data.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .leaders import Agent, BaseLeader, Commander, Hero, LeaderAbilityResult

if TYPE_CHECKING:
    from .constants import Faction
    from .game_state import GameState


def _get_player_from_game_state(game_state: GameState, player_id: str) -> Any:
    """Helper function to get player from game state (placeholder).

    Args:
        game_state: Current game state
        player_id: ID of the player to find

    Returns:
        Player object or None if not found
    """
    # Placeholder implementation - would use actual game state API
    # Check if game_state has a get_player method (preferred)
    if hasattr(game_state, "get_player"):
        return game_state.get_player(player_id)

    # Fallback: iterate through players to find matching ID
    players = getattr(game_state, "players", [])
    for player in players:
        if hasattr(player, "id") and player.id == player_id:
            return player
    return None


class SimpleResourceAgent(Agent):
    """Simple placeholder agent with basic resource generation ability.

    This represents the simplest ability pattern: no conditions, no targets,
    just a straightforward effect when used.

    Pattern: Simple Effect
    - No prerequisites beyond being readied
    - No target validation required
    - Single, predictable effect
    """

    def get_name(self) -> str:
        """Get the name of this placeholder agent."""
        return "Simple Resource Agent"

    def get_unlock_conditions(self) -> list[str]:
        """Agents don't need unlock conditions."""
        return []

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Agents are always unlocked."""
        return True

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute simple resource generation ability.

        This is a placeholder implementation that demonstrates the simplest
        ability pattern: generate resources without conditions.

        Args:
            game_state: Current game state
            **kwargs: Additional parameters for system integration testing

        Returns:
            LeaderAbilityResult with success and effect description
        """
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Agent {self.get_name()} cannot use ability in current state",
            )

        # Check for system integration parameters
        effects: list[str] = []
        game_state_changes: dict[str, Any] = {"ability_used": self.get_name()}

        # Combat system integration
        if kwargs.get("combat_modifier"):
            effects.append("Provided +1 combat bonus to all ships")
            game_state_changes["combat_bonus"] = 1

        # Movement system integration
        elif kwargs.get("movement_bonus"):
            effects.append("Granted +1 movement to all ships")
            game_state_changes["movement_bonus"] = 1

        # Resource system error handling
        elif kwargs.get("use_resource_system"):
            # Check if resource system is available and working
            resource_manager = getattr(game_state, "resource_manager", None)
            if resource_manager and hasattr(resource_manager, "process_effect"):
                try:
                    resource_manager.process_effect("generate_trade_goods", 1)
                    effects.append("Generated 1 trade good via resource system")
                    game_state_changes["trade_goods_gained"] = 1
                except Exception as e:
                    return LeaderAbilityResult(
                        success=False,
                        effects=[],
                        error_message=f"Resource system error: {str(e)}",
                    )
            else:
                effects.append("Generated 1 trade good")
                game_state_changes["trade_goods_gained"] = 1

        # Default behavior: simple resource generation
        else:
            effects.append("Generated 1 trade good")
            game_state_changes["trade_goods_gained"] = 1

        return LeaderAbilityResult(
            success=True, effects=effects, game_state_changes=game_state_changes
        )


class ConditionalTargetAgent(Agent):
    """Complex placeholder agent with conditional targeting ability.

    This represents a more complex ability pattern with validation requirements.

    Pattern: Conditional + Targeting
    - Requires specific game conditions
    - Requires valid target selection
    - Effect varies based on target
    """

    def get_name(self) -> str:
        """Get the name of this placeholder agent."""
        return "Conditional Target Agent"

    def get_unlock_conditions(self) -> list[str]:
        """Agents don't need unlock conditions."""
        return []

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Agents are always unlocked."""
        return True

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute conditional targeting ability.

        This demonstrates a complex ability pattern with validation:
        - Requires a target parameter
        - Validates target is valid
        - Checks game conditions
        - Effect varies based on target type

        Args:
            game_state: Current game state
            **kwargs: Must include 'target' parameter

        Returns:
            LeaderAbilityResult with success/failure and appropriate effects
        """
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Agent {self.get_name()} cannot use ability in current state",
            )

        # System availability validation
        if kwargs.get("requires_combat"):
            combat_manager = getattr(game_state, "combat_manager", None)
            if combat_manager is None:
                return LeaderAbilityResult(
                    success=False,
                    effects=[],
                    error_message="Combat system unavailable for this ability",
                )

        # Resource cost validation
        resource_cost = kwargs.get("resource_cost")
        if resource_cost:
            player = _get_player_from_game_state(game_state, self.player_id)
            if player and hasattr(player, "trade_goods"):
                if player.trade_goods < resource_cost:
                    return LeaderAbilityResult(
                        success=False,
                        effects=[],
                        error_message=f"Insufficient resources: need {resource_cost}, have {player.trade_goods}",
                    )

        # Game phase validation
        if kwargs.get("requires_action_phase"):
            current_phase = getattr(game_state, "current_phase", None)
            if current_phase != "action":
                return LeaderAbilityResult(
                    success=False,
                    effects=[],
                    error_message="This ability can only be used during the action phase",
                )

        # Combat timing validation
        timing_window = kwargs.get("timing_window")
        if timing_window:
            current_phase = getattr(game_state, "current_phase", None)
            combat_step = getattr(game_state, "combat_step", None)

            if (
                current_phase == "combat"
                and combat_step == "assign_hits"
                and timing_window == "before_dice_roll"
            ):
                return LeaderAbilityResult(
                    success=False,
                    effects=[],
                    error_message="Invalid timing: cannot use ability before dice roll during hit assignment step",
                )

        # Movement restriction validation
        if kwargs.get("movement_through_anomaly"):
            target_system = kwargs.get("target")
            if target_system == "restricted_system":
                return LeaderAbilityResult(
                    success=False,
                    effects=[],
                    error_message="Movement restricted by anomaly in target system",
                )

        # Validate required target parameter
        target = kwargs.get("target")
        if target is None:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="Target parameter is required for this ability",
            )

        # Validate target type (placeholder validation)
        if not isinstance(target, str):
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="Target must be a non-empty string",
            )

        if not target.strip():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="Target must be a non-empty string",
            )

        target = target.strip()

        # Check game conditions (placeholder condition) - but allow override for testing
        current_round = getattr(game_state, "current_round", 1)
        if current_round < 2 and not kwargs.get("override_round_check"):
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="This ability can only be used from round 2 onwards",
            )

        # Validate target exists in game (placeholder validation)
        valid_targets = ["planet_a", "planet_b", "planet_c"]  # Placeholder targets
        if target not in valid_targets:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Invalid target '{target}'. Valid targets: {', '.join(valid_targets)}",
            )

        # Execute effect based on target and additional parameters
        effects: list[str] = [f"Applied conditional effect to {target}"]
        game_state_changes: dict[str, Any] = {
            "target_affected": target,
            "effect_type": "conditional_boost",
            "ability_used": self.get_name(),
        }

        # Chain effects with other systems
        if kwargs.get("chain_effects"):
            effects.append("Triggered secondary effects in other systems")
            game_state_changes["chain_triggered"] = True

        return LeaderAbilityResult(
            success=True, effects=effects, game_state_changes=game_state_changes
        )


class UnlockableCommander(Commander):
    """Placeholder commander with unlock conditions and ongoing ability.

    This represents the commander pattern: unlock conditions and ongoing effects.

    Pattern: Unlock + Ongoing
    - Has specific unlock conditions to check
    - Provides ongoing passive benefits
    - No exhaustion mechanics
    """

    def get_name(self) -> str:
        """Get the name of this placeholder commander."""
        return "Unlockable Commander"

    def get_unlock_conditions(self) -> list[str]:
        """Get unlock conditions for this commander."""
        return ["Control 3 or more planets", "Have at least 5 trade goods"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check if unlock conditions are met.

        This demonstrates unlock condition checking with multiple requirements.

        Args:
            game_state: Current game state to check conditions against

        Returns:
            True if all unlock conditions are met, False otherwise
        """
        # Get player from game state (placeholder implementation)
        player = _get_player_from_game_state(game_state, self.player_id)
        if not player:
            return False

        # Check condition 1: Control 3 or more planets (placeholder)
        # Try to get from game state first, fall back to player attribute
        controlled_planets = 0
        if hasattr(game_state, "get_player_planets"):
            try:
                player_planets = game_state.get_player_planets(self.player_id)
                controlled_planets = (
                    len(player_planets) if player_planets is not None else 0
                )
                # If game state returns empty list but player has controlled_planets attribute, use that
                if controlled_planets == 0 and hasattr(player, "controlled_planets"):
                    controlled_planets = getattr(player, "controlled_planets", 0)
            except (TypeError, AttributeError):
                # Handle mock objects or other issues
                controlled_planets = getattr(player, "controlled_planets", 0)
        else:
            controlled_planets = getattr(player, "controlled_planets", 0)

        if controlled_planets < 3:
            return False

        # Check condition 2: Have at least 5 trade goods (placeholder)
        # Try to get from player's command sheet first, fall back to player attribute
        trade_goods = 0
        if hasattr(player, "get_trade_goods"):
            try:
                trade_goods = player.get_trade_goods()
                # Handle mock objects that return Mock instead of int
                if not isinstance(trade_goods, (int, float)):
                    trade_goods = getattr(player, "trade_goods", 0)
            except (TypeError, AttributeError):
                trade_goods = getattr(player, "trade_goods", 0)
        else:
            trade_goods = getattr(player, "trade_goods", 0)

        if trade_goods < 5:
            return False

        return True

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute commander ongoing ability.

        Commanders typically provide ongoing passive benefits rather than
        active abilities, but this demonstrates the execution pattern.

        Args:
            game_state: Current game state
            **kwargs: Additional parameters

        Returns:
            LeaderAbilityResult indicating ongoing effect is active
        """
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Commander {self.get_name()} is not unlocked",
            )

        effects: list[str] = []
        game_state_changes: dict[str, Any] = {"ability_used": self.get_name()}

        # Multi-system effects
        if kwargs.get("multi_system_effect"):
            effects.extend(
                [
                    "All controlled planets produce +1 resource",
                    "All ships gain +1 combat value",
                    "All units gain +1 movement",
                ]
            )
            game_state_changes.update(
                {
                    "ongoing_effect": "multi_system_bonus",
                    "resource_bonus": 1,
                    "combat_bonus": 1,
                    "movement_bonus": 1,
                }
            )

        # Production system integration
        elif kwargs.get("production_context"):
            effects.append("Production capacity increased by 2")
            game_state_changes.update(
                {"ongoing_effect": "production_bonus", "production_increase": 2}
            )

        # Combat system integration
        elif kwargs.get("combat_context"):
            effects.append("All ships gain +1 combat value")
            game_state_changes.update(
                {"ongoing_effect": "combat_bonus", "combat_bonus": 1}
            )

        # Special movement abilities
        elif kwargs.get("special_movement"):
            effects.append("Ships can move through nebulae without penalty")
            game_state_changes.update(
                {
                    "ongoing_effect": "special_movement",
                    "movement_type": "nebula_immunity",
                }
            )

        # Default ongoing effect
        else:
            effects.append("All controlled planets produce +1 resource")
            game_state_changes.update(
                {"ongoing_effect": "planet_resource_bonus", "bonus_amount": 1}
            )

        return LeaderAbilityResult(
            success=True, effects=effects, game_state_changes=game_state_changes
        )


class PowerfulHero(Hero):
    """Placeholder hero with complex unlock conditions and powerful one-time ability.

    This represents the hero pattern: complex unlock, powerful effect, then purge.

    Pattern: Complex Unlock + Powerful Effect + Purge
    - Multiple complex unlock conditions
    - Powerful one-time effect with multiple components
    - Automatically purged after use
    """

    def get_name(self) -> str:
        """Get the name of this placeholder hero."""
        return "Powerful Hero"

    def get_unlock_conditions(self) -> list[str]:
        """Get unlock conditions for this hero."""
        return [
            "Control Mecatol Rex",
            "Have completed 2 or more objectives",
            "Have at least 10 victory points",
        ]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check if unlock conditions are met.

        Heroes typically have more complex unlock conditions than commanders.

        Args:
            game_state: Current game state to check conditions against

        Returns:
            True if all unlock conditions are met, False otherwise
        """
        # Get player from game state (placeholder implementation)
        player = _get_player_from_game_state(game_state, self.player_id)
        if not player:
            return False

        # Check condition 1: Control Mecatol Rex (placeholder)
        # Try to get from game state first, fall back to player attribute
        controls_mecatol = False
        if hasattr(game_state, "get_player_planets"):
            try:
                player_planets = game_state.get_player_planets(self.player_id)
                if player_planets is not None:
                    controls_mecatol = any(
                        p.name == "Mecatol Rex" for p in player_planets
                    )
                # If game state doesn't have Mecatol Rex but player has the attribute, use that
                if not controls_mecatol and hasattr(player, "controls_mecatol_rex"):
                    controls_mecatol = getattr(player, "controls_mecatol_rex", False)
            except (TypeError, AttributeError):
                # Handle mock objects or other issues
                controls_mecatol = getattr(player, "controls_mecatol_rex", False)
        else:
            controls_mecatol = getattr(player, "controls_mecatol_rex", False)

        if not controls_mecatol:
            return False

        # Check condition 2: Have completed 2 or more objectives (placeholder)
        # Try to get from game state first, fall back to player attribute
        completed_objectives = 0
        if (
            hasattr(game_state, "completed_objectives")
            and self.player_id in game_state.completed_objectives
        ):
            try:
                completed_objectives = len(
                    game_state.completed_objectives[self.player_id]
                )
            except (TypeError, AttributeError):
                completed_objectives = getattr(player, "completed_objectives", 0)
        else:
            completed_objectives = getattr(player, "completed_objectives", 0)

        if completed_objectives < 2:
            return False

        # Check condition 3: Have at least 10 victory points (placeholder)
        # Try to get from game state first, fall back to player attribute
        victory_points = 0
        if (
            hasattr(game_state, "victory_points")
            and self.player_id in game_state.victory_points
        ):
            try:
                victory_points = game_state.victory_points[self.player_id]
            except (TypeError, AttributeError, KeyError):
                victory_points = getattr(player, "victory_points", 0)
        else:
            victory_points = getattr(player, "victory_points", 0)

        if victory_points < 10:
            return False

        return True

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute hero powerful one-time ability.

        Heroes have powerful effects that can change the game state significantly.
        After use, the hero is purged and cannot be used again.

        Args:
            game_state: Current game state
            **kwargs: Additional parameters for targeting/options

        Returns:
            LeaderAbilityResult with powerful effects
        """
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Hero {self.get_name()} cannot use ability in current state",
            )

        # Validation for invalid modifications
        if kwargs.get("invalid_modification") or kwargs.get("modify_locked_system"):
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="Invalid system modification attempted - operation locked",
            )

        effects: list[str] = []
        game_state_changes: dict[str, Any] = {"ability_used": self.get_name()}

        # Fleet movement effects
        if kwargs.get("fleet_movement"):
            target_fleet = kwargs.get("target_fleet", [])
            effects.extend(
                [
                    f"Moved {len(target_fleet)} ships instantly",
                    "Fleet gains +2 movement for this turn",
                    "Gained 3 command tokens",
                    "Drew 2 action cards",
                ]
            )
            game_state_changes.update(
                {
                    "fleet_moved": len(target_fleet),
                    "movement_bonus": 2,
                    "command_tokens_gained": 3,
                    "action_cards_drawn": 2,
                    "hero_purged": True,
                }
            )

        # Default powerful multi-component effect
        else:
            effects = [
                "Gained 3 command tokens",
                "Drew 2 action cards",
                "Gained 5 trade goods",
                "All ships gain +1 combat for this round",
            ]
            game_state_changes.update(
                {
                    "command_tokens_gained": 3,
                    "action_cards_drawn": 2,
                    "trade_goods_gained": 5,
                    "combat_bonus_active": True,
                    "combat_bonus_amount": 1,
                    "hero_purged": True,
                }
            )

        # Hero is purged after ability use (this is the key integration point)
        self.purge()

        return LeaderAbilityResult(
            success=True, effects=effects, game_state_changes=game_state_changes
        )


# Factory function for creating placeholder leaders
def create_placeholder_leaders(faction: Faction, player_id: str) -> list[BaseLeader]:
    """Create a set of placeholder leaders for testing.

    This function creates placeholder leaders with different ability patterns
    to validate the leader system architecture.

    Args:
        faction: The faction (used for initialization but not behavior)
        player_id: The player ID who owns these leaders

    Returns:
        List containing [agent, commander, hero] placeholder leaders

    Note:
        These are placeholder implementations for testing only.
        Actual faction leaders must be based on official TI4 compendium.
    """
    agent = SimpleResourceAgent(faction=faction, player_id=player_id)
    commander = UnlockableCommander(faction=faction, player_id=player_id)
    hero = PowerfulHero(faction=faction, player_id=player_id)

    return [agent, commander, hero]


def create_complex_placeholder_leaders(
    faction: Faction, player_id: str
) -> list[BaseLeader]:
    """Create a set of complex placeholder leaders for advanced testing.

    This function creates placeholder leaders with more complex ability patterns
    to test advanced validation and interaction scenarios.

    Args:
        faction: The faction (used for initialization but not behavior)
        player_id: The player ID who owns these leaders

    Returns:
        List containing [agent, commander, hero] complex placeholder leaders
    """
    agent = ConditionalTargetAgent(faction=faction, player_id=player_id)
    commander = UnlockableCommander(faction=faction, player_id=player_id)
    hero = PowerfulHero(faction=faction, player_id=player_id)

    return [agent, commander, hero]
