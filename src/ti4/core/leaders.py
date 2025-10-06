"""Leader system implementation for TI4 Rule 51: LEADERS.

This module implements the core leader system including:
- Leader types (Agent, Commander, Hero)
- Leader state management (locked/unlocked, readied/exhausted, purged)
- Base leader class and ability result structures

LRR References:
- Rule 51: LEADERS
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .constants import Faction
    from .game_state import GameState
    from .player import Player


class LeaderType(Enum):
    """Enumeration of leader types as defined in Rule 51."""

    AGENT = "agent"
    COMMANDER = "commander"
    HERO = "hero"


class LeaderLockStatus(Enum):
    """Enumeration of leader lock states for state management."""

    LOCKED = "locked"
    UNLOCKED = "unlocked"
    PURGED = "purged"  # Heroes only - permanent removal


class LeaderReadyStatus(Enum):
    """Enumeration of leader ready states for agent mechanics."""

    READIED = "readied"
    EXHAUSTED = "exhausted"


@dataclass
class LeaderAbilityResult:
    """Result of leader ability execution with standardized outcomes.

    Provides consistent structure for ability results across all leader types.
    """

    success: bool
    effects: list[str]
    error_message: str | None = None
    game_state_changes: dict[str, Any] | None = None


@dataclass
class LeaderSheet:
    """Leader sheet data structure to hold a player's three leaders.

    Each player has exactly three leaders: one agent, one commander, and one hero.
    The leader sheet provides methods to access leaders by type and retrieve all leaders.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 5.1, 5.2, 5.3, 5.4, 5.5

    Attributes:
        player_id: The ID of the player who owns this leader sheet
        agent: The player's agent leader (optional during initialization)
        commander: The player's commander leader (optional during initialization)
        hero: The player's hero leader (optional during initialization)
    """

    player_id: str
    agent: Agent | None = None
    commander: Commander | None = None
    hero: Hero | None = None

    def __post_init__(self) -> None:
        """Validate leader sheet after initialization.

        Raises:
            ValueError: If player_id is empty or None
        """
        if not self.player_id or not self.player_id.strip():
            raise ValueError("player_id cannot be empty or None")

    def get_all_leaders(self) -> list[BaseLeader]:
        """Get all leaders on this leader sheet.

        Returns:
            List of all non-None leaders (agent, commander, hero)

        Note:
            The order is consistent: agent, commander, hero (when present)
        """
        leaders: list[BaseLeader] = []
        if self.agent is not None:
            leaders.append(self.agent)
        if self.commander is not None:
            leaders.append(self.commander)
        if self.hero is not None:
            leaders.append(self.hero)
        return leaders

    def get_leader_by_type(self, leader_type: LeaderType) -> BaseLeader | None:
        """Get a leader by its type.

        Args:
            leader_type: The type of leader to retrieve (AGENT, COMMANDER, or HERO)

        Returns:
            The leader of the specified type, or None if not present

        Raises:
            ValueError: If leader_type is not a valid LeaderType enum value
        """
        if not isinstance(leader_type, LeaderType):
            raise ValueError("leader_type must be a LeaderType enum value")

        type_map = {
            LeaderType.AGENT: self.agent,
            LeaderType.COMMANDER: self.commander,
            LeaderType.HERO: self.hero,
        }
        return type_map[leader_type]

    def get_leader_by_name(self, name: str) -> BaseLeader | None:
        """Get a leader by its name.

        Args:
            name: The name of the leader to find

        Returns:
            The leader with the specified name, or None if not found

        Raises:
            ValueError: If name is empty or None
        """
        if not name or not name.strip():
            raise ValueError("name cannot be empty or None")

        name = name.strip()
        for leader in self.get_all_leaders():
            if leader.get_name() == name:
                return leader
        return None

    def _validate_leader_assignment(
        self, leader: BaseLeader | None, expected_type: type[BaseLeader], type_name: str
    ) -> None:
        """Validate leader assignment parameters.

        Args:
            leader: The leader to validate
            expected_type: The expected type of the leader
            type_name: The name of the leader type for error messages

        Raises:
            ValueError: If validation fails
        """
        if leader is None:
            raise ValueError(f"{type_name.lower()} cannot be None")
        if not isinstance(leader, expected_type):
            raise ValueError(
                f"{type_name.lower()} must be a {expected_type.__name__} instance"
            )
        if leader.player_id != self.player_id:
            raise ValueError(
                f"{expected_type.__name__} belongs to player {leader.player_id}, "
                f"but sheet belongs to player {self.player_id}"
            )

    def set_agent(self, agent: Agent) -> None:
        """Set the agent leader for this sheet.

        Args:
            agent: The agent leader to set

        Raises:
            ValueError: If agent is None or not an Agent instance
            ValueError: If agent belongs to a different player
        """
        self._validate_leader_assignment(agent, Agent, "Agent")
        self.agent = agent

    def set_commander(self, commander: Commander) -> None:
        """Set the commander leader for this sheet.

        Args:
            commander: The commander leader to set

        Raises:
            ValueError: If commander is None or not a Commander instance
            ValueError: If commander belongs to a different player
        """
        self._validate_leader_assignment(commander, Commander, "Commander")
        self.commander = commander

    def set_hero(self, hero: Hero) -> None:
        """Set the hero leader for this sheet.

        Args:
            hero: The hero leader to set

        Raises:
            ValueError: If hero is None or not a Hero instance
            ValueError: If hero belongs to a different player
        """
        self._validate_leader_assignment(hero, Hero, "Hero")
        self.hero = hero

    def is_complete(self) -> bool:
        """Check if the leader sheet has all three leaders assigned.

        Returns:
            True if agent, commander, and hero are all present, False otherwise
        """
        return (
            self.agent is not None
            and self.commander is not None
            and self.hero is not None
        )

    def serialize_for_persistence(self) -> dict[str, Any]:
        """Serialize leader sheet for persistence.

        Returns:
            Dictionary containing all leader sheet data for persistence

        LRR References:
        - Rule 51: LEADERS
        - Requirements 8.2, 8.3
        """
        return {
            "player_id": self.player_id,
            "agent": self.agent.serialize_state() if self.agent else None,
            "commander": self.commander.serialize_state() if self.commander else None,
            "hero": self.hero.serialize_state() if self.hero else None,
        }

    @classmethod
    def from_serialized_data(cls, serialized_data: dict[str, Any]) -> LeaderSheet:
        """Create LeaderSheet from serialized data.

        Args:
            serialized_data: Dictionary containing serialized leader sheet data

        Returns:
            LeaderSheet instance restored from serialized data

        Raises:
            ValueError: If serialized_data is invalid or missing required fields

        LRR References:
        - Rule 51: LEADERS
        - Requirements 8.2, 8.3
        """
        if not isinstance(serialized_data, dict):
            raise ValueError("serialized_data must be a dictionary")

        if "player_id" not in serialized_data:
            raise ValueError("serialized_data must contain 'player_id'")

        player_id = serialized_data["player_id"]
        leader_sheet = cls(player_id=player_id)

        # Restore agent if present
        if serialized_data.get("agent"):
            agent = BaseLeader.from_serialized_state(serialized_data["agent"])
            leader_sheet.set_agent(agent)  # type: ignore

        # Restore commander if present
        if serialized_data.get("commander"):
            commander = BaseLeader.from_serialized_state(serialized_data["commander"])
            leader_sheet.set_commander(commander)  # type: ignore

        # Restore hero if present
        if serialized_data.get("hero"):
            hero = BaseLeader.from_serialized_state(serialized_data["hero"])
            leader_sheet.set_hero(hero)  # type: ignore

        return leader_sheet


class BaseLeader(ABC):
    """Abstract base class for all leader types.

    Defines the common interface and state management for agents, commanders, and heroes.
    Each leader type must implement specific behavior for unlock conditions and abilities.
    """

    def __init__(self, faction: Faction, player_id: str) -> None:
        """Initialize a leader with faction and player ownership.

        Args:
            faction: The faction this leader belongs to
            player_id: The ID of the player who owns this leader

        Raises:
            ValueError: If player_id is empty or None
            TypeError: If faction is not a Faction enum value
        """
        if not player_id or not player_id.strip():
            raise ValueError("player_id cannot be empty or None")

        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        if not isinstance(faction, FactionEnum):
            raise TypeError("faction must be a Faction enum value")

        self.faction = faction
        self.player_id = player_id.strip()
        self.lock_status = self._get_initial_lock_status()
        self.ready_status = self._get_initial_ready_status()

    @abstractmethod
    def get_leader_type(self) -> LeaderType:
        """Get the type of this leader (agent, commander, or hero)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this leader."""
        pass

    @abstractmethod
    def get_unlock_conditions(self) -> list[str]:
        """Get the unlock conditions for this leader."""
        pass

    @abstractmethod
    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check if this leader's unlock conditions are met."""
        pass

    @abstractmethod
    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute this leader's ability."""
        pass

    @abstractmethod
    def _get_initial_lock_status(self) -> LeaderLockStatus:
        """Get the initial lock status for this leader type."""
        pass

    @abstractmethod
    def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
        """Get the initial ready status for this leader type (None if not applicable)."""
        pass

    @abstractmethod
    def can_use_ability(self) -> bool:
        """Check if this leader can use their ability in the current state."""
        pass

    @abstractmethod
    def unlock(self) -> None:
        """Unlock this leader if applicable."""
        pass

    def serialize_state(self) -> dict[str, Any]:
        """Serialize leader state for persistence.

        Returns:
            Dictionary containing leader state data

        LRR References:
        - Rule 51: LEADERS
        - Requirements 8.2, 8.3
        """
        return {
            "faction": self.faction.value,
            "player_id": self.player_id,
            "lock_status": self.lock_status.value,
            "ready_status": self.ready_status.value if self.ready_status else None,
            "leader_type": self.get_leader_type().value,
            "name": self.get_name(),
        }

    @classmethod
    def from_serialized_state(cls, serialized_data: dict[str, Any]) -> BaseLeader:
        """Create leader from serialized state data.

        Args:
            serialized_data: Dictionary containing serialized leader data

        Returns:
            Leader instance restored from serialized data

        Raises:
            ValueError: If serialized_data is invalid or missing required fields

        LRR References:
        - Rule 51: LEADERS
        - Requirements 8.2, 8.3
        """
        if not isinstance(serialized_data, dict):
            raise ValueError("serialized_data must be a dictionary")

        required_fields = ["faction", "player_id", "leader_type", "name"]
        for field in required_fields:
            if field not in serialized_data:
                raise ValueError(f"serialized_data must contain '{field}'")

        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        # Get faction enum
        faction_str = serialized_data["faction"]
        try:
            faction = FactionEnum(faction_str)
        except ValueError as e:
            raise ValueError(f"Invalid faction: {faction_str}") from e

        # Get leader type and create appropriate instance
        leader_type_str = serialized_data["leader_type"]
        player_id = serialized_data["player_id"]
        leader_name = serialized_data.get("name", "")

        # Try to create specific leader based on name, fall back to generic types
        leader: BaseLeader
        if leader_name == "Simple Resource Agent":
            from .placeholder_leaders import SimpleResourceAgent

            leader = SimpleResourceAgent(faction=faction, player_id=player_id)
        elif leader_name == "Conditional Target Agent":
            from .placeholder_leaders import ConditionalTargetAgent

            leader = ConditionalTargetAgent(faction=faction, player_id=player_id)
        elif leader_name == "Unlockable Commander":
            from .placeholder_leaders import UnlockableCommander

            leader = UnlockableCommander(faction=faction, player_id=player_id)
        elif leader_name == "Powerful Hero":
            from .placeholder_leaders import PowerfulHero

            leader = PowerfulHero(faction=faction, player_id=player_id)
        elif leader_type_str == "agent":
            leader = Agent(faction=faction, player_id=player_id)
        elif leader_type_str == "commander":
            leader = Commander(faction=faction, player_id=player_id)
        elif leader_type_str == "hero":
            leader = Hero(faction=faction, player_id=player_id)
        else:
            raise ValueError(f"Invalid leader_type: {leader_type_str}")

        # Restore lock status
        if "lock_status" in serialized_data:
            lock_status_str = serialized_data["lock_status"]
            try:
                leader.lock_status = LeaderLockStatus(lock_status_str)
            except ValueError as e:
                raise ValueError(f"Invalid lock_status: {lock_status_str}") from e

        # Restore ready status (if applicable)
        if "ready_status" in serialized_data and serialized_data["ready_status"]:
            ready_status_str = serialized_data["ready_status"]
            try:
                leader.ready_status = LeaderReadyStatus(ready_status_str)
            except ValueError as e:
                raise ValueError(f"Invalid ready_status: {ready_status_str}") from e

        return leader


class Agent(BaseLeader):
    """Agent leader type with ready/exhaust mechanics.

    Agents start unlocked and readied, can be exhausted when abilities are used,
    and are automatically readied during the status phase.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 2.1, 2.2, 2.3, 2.4, 2.5
    """

    def get_leader_type(self) -> LeaderType:
        """Get the leader type for agents."""
        return LeaderType.AGENT

    def get_name(self) -> str:
        """Get the name of this agent (placeholder implementation)."""
        return "Agent"

    def get_unlock_conditions(self) -> list[str]:
        """Get unlock conditions for agents (none - they start unlocked)."""
        return []

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check unlock conditions for agents (always True - they start unlocked)."""
        return True

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute agent ability (placeholder implementation)."""
        return LeaderAbilityResult(success=True, effects=["Agent ability executed"])

    def _get_initial_lock_status(self) -> LeaderLockStatus:
        """Agents start unlocked."""
        return LeaderLockStatus.UNLOCKED

    def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
        """Agents start readied."""
        return LeaderReadyStatus.READIED

    def can_use_ability(self) -> bool:
        """Check if agent can use ability (must be unlocked and readied)."""
        return (
            self.lock_status == LeaderLockStatus.UNLOCKED
            and self.ready_status == LeaderReadyStatus.READIED
        )

    def exhaust(self) -> None:
        """Exhaust the agent (change state from readied to exhausted).

        Raises:
            LeaderStateError: If agent is not in readied state
        """
        if self.ready_status != LeaderReadyStatus.READIED:
            status_str = self.ready_status.value if self.ready_status else "None"
            raise LeaderStateError.for_invalid_transition(
                self, "exhaust", f"already_{status_str}"
            )
        self.ready_status = LeaderReadyStatus.EXHAUSTED

    def ready(self) -> None:
        """Ready the agent (change state from exhausted to readied).

        Raises:
            ValueError: If agent is not in exhausted state
        """
        if self.ready_status != LeaderReadyStatus.EXHAUSTED:
            status_str = self.ready_status.value if self.ready_status else "None"
            raise ValueError(
                f"Cannot ready agent in {status_str} state. "
                "Agent must be exhausted to be readied."
            )
        self.ready_status = LeaderReadyStatus.READIED

    def unlock(self) -> None:
        """Agents don't need to be unlocked - they start unlocked."""
        pass  # Agents are always unlocked


class Commander(BaseLeader):
    """Commander leader type with unlock mechanics.

    Commanders start locked and must meet specific conditions to unlock.
    Once unlocked, they provide ongoing abilities without exhaustion.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
    """

    def get_leader_type(self) -> LeaderType:
        """Get the leader type for commanders."""
        return LeaderType.COMMANDER

    def get_name(self) -> str:
        """Get the name of this commander (placeholder implementation)."""
        return "Commander"

    def get_unlock_conditions(self) -> list[str]:
        """Get unlock conditions for commanders (placeholder implementation)."""
        return ["Placeholder unlock condition"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check unlock conditions for commanders (placeholder implementation)."""
        return False

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute commander ability (placeholder implementation)."""
        return LeaderAbilityResult(success=True, effects=["Commander ability executed"])

    def _get_initial_lock_status(self) -> LeaderLockStatus:
        """Commanders start locked."""
        return LeaderLockStatus.LOCKED

    def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
        """Commanders don't have ready/exhaust states."""
        return None

    def can_use_ability(self) -> bool:
        """Check if commander can use ability (must be unlocked)."""
        return self.lock_status == LeaderLockStatus.UNLOCKED

    def unlock(self) -> None:
        """Unlock the commander (change state from locked to unlocked)."""
        if self.lock_status == LeaderLockStatus.LOCKED:
            self.lock_status = LeaderLockStatus.UNLOCKED


class Hero(BaseLeader):
    """Hero leader type with unlock and purge mechanics.

    Heroes start locked and must meet specific conditions to unlock.
    Once unlocked, they can use their powerful one-time ability and are then purged.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
    """

    def get_leader_type(self) -> LeaderType:
        """Get the leader type for heroes."""
        return LeaderType.HERO

    def get_name(self) -> str:
        """Get the name of this hero (placeholder implementation)."""
        return "Hero"

    def get_unlock_conditions(self) -> list[str]:
        """Get unlock conditions for heroes (placeholder implementation)."""
        return ["Placeholder unlock condition"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        """Check unlock conditions for heroes (placeholder implementation)."""
        return False

    def execute_ability(
        self, game_state: GameState, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute hero ability (placeholder implementation)."""
        return LeaderAbilityResult(success=True, effects=["Hero ability executed"])

    def _get_initial_lock_status(self) -> LeaderLockStatus:
        """Heroes start locked."""
        return LeaderLockStatus.LOCKED

    def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
        """Heroes don't have ready/exhaust states."""
        return None

    def can_use_ability(self) -> bool:
        """Check if hero can use ability (must be unlocked but not purged).

        Returns:
            True if hero is unlocked and not purged, False otherwise
        """
        return self.lock_status == LeaderLockStatus.UNLOCKED

    def unlock(self) -> None:
        """Unlock the hero (change state from locked to unlocked).

        Heroes can only be unlocked from the locked state. Once unlocked,
        they remain unlocked until purged.

        Raises:
            LeaderUnlockError: If hero is already purged (cannot unlock purged heroes)
        """
        if self.lock_status == LeaderLockStatus.PURGED:
            raise LeaderUnlockError.for_purged_hero(self)

        if self.lock_status == LeaderLockStatus.LOCKED:
            self.lock_status = LeaderLockStatus.UNLOCKED

    def purge(self) -> None:
        """Purge the hero (change state to purged, making abilities permanently unavailable).

        Heroes can be purged from any state (locked or unlocked). Once purged,
        they cannot be unlocked or use abilities again.

        Note:
            This is typically called after a hero ability is used, as per Rule 51.
        """
        self.lock_status = LeaderLockStatus.PURGED


# Leader initialization functions for game setup


def initialize_player_leaders(player: Player) -> None:
    """Initialize leaders for a player during game setup.

    Creates and assigns all three leaders (agent, commander, hero) to the player's
    leader sheet using the LeaderRegistry. Each leader is created with the player's
    faction and proper initial states.

    Args:
        player: The player to initialize leaders for

    Raises:
        ValueError: If leaders are already initialized for this player

    LRR References:
    - Rule 51: LEADERS
    - Requirements 5.1, 5.2, 5.3, 5.4, 5.5
    """
    if player.leader_sheet.is_complete():
        raise ValueError("Leaders already initialized for this player")

    # Use the registry to create faction-specific leaders
    registry = LeaderRegistry()
    leaders = registry.create_faction_leaders(player.faction, player.id)

    # Assign them to the leader sheet (agent, commander, hero order)
    player.leader_sheet.set_agent(leaders[0])  # type: ignore
    player.leader_sheet.set_commander(leaders[1])  # type: ignore
    player.leader_sheet.set_hero(leaders[2])  # type: ignore


def setup_player_leaders_for_game(player: Player, game_state: GameState) -> None:
    """Setup leaders for a player being added to an existing game.

    This is a wrapper around initialize_player_leaders that can be used when
    adding players to existing games. Currently just calls initialize_player_leaders
    but could be extended for game-specific setup in the future.

    Args:
        player: The player to setup leaders for
        game_state: The game state (for future extensibility)

    LRR References:
    - Rule 51: LEADERS
    - Requirements 5.1, 5.2, 5.3, 5.4, 5.5
    """
    initialize_player_leaders(player)


# Leader-specific exceptions for error handling


class LeaderError(Exception):
    """Base exception for leader-related errors with context information.

    Provides a comprehensive base for all leader-related exceptions with
    support for context information, error message formatting, and
    serialization for logging purposes.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 8.4, 9.5

    Attributes:
        context: Dictionary containing contextual information about the error
    """

    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Initialize LeaderError with message and optional context.

        Args:
            message: The error message
            context: Optional dictionary containing contextual information
        """
        super().__init__(message)
        self.context = context or {}

    def get_context_value(self, key: str) -> Any:
        """Get a value from the error context.

        Args:
            key: The context key to retrieve

        Returns:
            The context value, or None if key doesn't exist
        """
        return self.context.get(key)

    def serialize_context(self) -> dict[str, Any]:
        """Serialize the error context for logging.

        Returns:
            Dictionary containing serializable context information
        """
        return dict(self.context)

    def get_filtered_context(
        self, exclude_keys: list[str] | None = None
    ) -> dict[str, Any]:
        """Get filtered context excluding sensitive information.

        Args:
            exclude_keys: List of keys to exclude from the context

        Returns:
            Filtered context dictionary
        """
        if exclude_keys is None:
            exclude_keys = []

        return {k: v for k, v in self.context.items() if k not in exclude_keys}

    def get_formatted_message(self) -> str:
        """Get formatted error message including context information.

        Returns:
            Formatted error message with relevant context
        """
        base_message = str(self)
        if not self.context:
            return base_message

        # Add relevant context to the message
        context_parts = []
        if "player_id" in self.context:
            context_parts.append(f"Player: {self.context['player_id']}")
        if "leader_name" in self.context:
            context_parts.append(f"Leader: {self.context['leader_name']}")

        if context_parts:
            return f"{base_message} ({', '.join(context_parts)})"
        return base_message


class LeaderNotFoundError(LeaderError):
    """Raised when a requested leader doesn't exist.

    Provides specific factory methods for different types of leader
    not found scenarios with appropriate context information.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    @classmethod
    def for_player(cls, player_id: str) -> LeaderNotFoundError:
        """Create LeaderNotFoundError for player not found scenario.

        Args:
            player_id: The ID of the player that was not found

        Returns:
            LeaderNotFoundError with player context
        """
        context = {"player_id": player_id, "error_type": "player_not_found"}
        return cls(f"Player {player_id} not found", context=context)

    @classmethod
    def for_leader_name(cls, leader_name: str, player_id: str) -> LeaderNotFoundError:
        """Create LeaderNotFoundError for leader name not found scenario.

        Args:
            leader_name: The name of the leader that was not found
            player_id: The ID of the player

        Returns:
            LeaderNotFoundError with leader name context
        """
        context = {
            "leader_name": leader_name,
            "player_id": player_id,
            "error_type": "leader_not_found",
        }
        return cls(
            f"Leader '{leader_name}' not found for player {player_id}", context=context
        )

    @classmethod
    def for_leader_type(
        cls, leader_type: LeaderType, player_id: str
    ) -> LeaderNotFoundError:
        """Create LeaderNotFoundError for leader type not found scenario.

        Args:
            leader_type: The type of leader that was not found
            player_id: The ID of the player

        Returns:
            LeaderNotFoundError with leader type context
        """
        context = {
            "leader_type": leader_type,
            "player_id": player_id,
            "error_type": "leader_type_not_found",
        }
        type_name = leader_type.value.title()
        return cls(
            f"{type_name} leader not found for player {player_id}", context=context
        )


class LeaderStateError(LeaderError):
    """Raised when leader is in invalid state for requested operation.

    Provides specific factory methods for different types of state
    errors with detailed context about the invalid state transition.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 8.4, 9.5
    """

    @classmethod
    def for_invalid_transition(
        cls, leader: BaseLeader, attempted_action: str, current_state: str
    ) -> LeaderStateError:
        """Create LeaderStateError for invalid state transition.

        Args:
            leader: The leader with invalid state
            attempted_action: The action that was attempted
            current_state: Description of the current invalid state

        Returns:
            LeaderStateError with transition context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "attempted_action": attempted_action,
            "current_state": current_state,
        }
        return cls(
            f"Cannot {attempted_action} {leader.get_name()} - already in {current_state} state",
            context=context,
        )

    @classmethod
    def for_ability_use_invalid_state(cls, leader: BaseLeader) -> LeaderStateError:
        """Create LeaderStateError for ability use in invalid state.

        Args:
            leader: The leader with invalid state for ability use

        Returns:
            LeaderStateError with ability use context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "current_lock_status": leader.lock_status,
            "current_ready_status": getattr(leader, "ready_status", None),
        }

        # Determine the specific reason based on leader type and state
        if isinstance(leader, Agent):
            if leader.ready_status == LeaderReadyStatus.EXHAUSTED:
                reason = "exhausted and cannot use abilities until readied"
            elif leader.lock_status != LeaderLockStatus.UNLOCKED:
                reason = "not unlocked"
            else:
                reason = "not in valid state for ability use"
        elif isinstance(leader, (Commander, Hero)):
            if leader.lock_status == LeaderLockStatus.LOCKED:
                reason = "locked and cannot use abilities until unlocked"
            elif leader.lock_status == LeaderLockStatus.PURGED:
                reason = "purged and can no longer use abilities"
            else:
                reason = "not in valid state for ability use"
        else:
            reason = "not in valid state for ability use"

        return cls(
            f"{leader.get_leader_type().value.title()} {leader.get_name()} cannot use ability - {reason}",
            context=context,
        )

    @classmethod
    def for_already_unlocked(cls, leader: BaseLeader) -> LeaderStateError:
        """Create LeaderStateError for attempting to unlock already unlocked leader.

        Args:
            leader: The leader that is already unlocked

        Returns:
            LeaderStateError with unlock context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "current_lock_status": leader.lock_status,
        }
        return cls(
            f"{leader.get_leader_type().value.title()} {leader.get_name()} is already unlocked",
            context=context,
        )


class LeaderUnlockError(LeaderError):
    """Raised when unlock conditions are not met.

    Provides specific factory methods for different types of unlock
    failures with detailed context about why unlocking failed.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    @classmethod
    def for_unmet_conditions(
        cls, leader: BaseLeader, unmet_conditions: list[str]
    ) -> LeaderUnlockError:
        """Create LeaderUnlockError for unmet unlock conditions.

        Args:
            leader: The leader that cannot be unlocked
            unmet_conditions: List of conditions that are not met

        Returns:
            LeaderUnlockError with conditions context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "unmet_conditions": unmet_conditions,
        }
        conditions_str = ", ".join(unmet_conditions)
        return cls(
            f"Cannot unlock {leader.get_name()} - unlock conditions not met: {conditions_str}",
            context=context,
        )

    @classmethod
    def for_purged_hero(cls, hero: BaseLeader) -> LeaderUnlockError:
        """Create LeaderUnlockError for attempting to unlock purged hero.

        Args:
            hero: The purged hero that cannot be unlocked

        Returns:
            LeaderUnlockError with purged hero context
        """
        context = {
            "leader_name": hero.get_name(),
            "leader_type": hero.get_leader_type(),
            "current_lock_status": hero.lock_status,
        }
        return cls(
            f"Cannot unlock purged hero {hero.get_name()} - heroes that have been purged cannot be unlocked again",
            context=context,
        )

    @classmethod
    def for_invalid_game_state(
        cls, leader: BaseLeader, game_state_issue: str
    ) -> LeaderUnlockError:
        """Create LeaderUnlockError for invalid game state preventing unlock.

        Args:
            leader: The leader that cannot be unlocked
            game_state_issue: Description of the game state issue

        Returns:
            LeaderUnlockError with game state context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "game_state_issue": game_state_issue,
        }
        return cls(
            f"Cannot unlock {leader.get_name()} due to game state: {game_state_issue}",
            context=context,
        )


class LeaderAbilityError(LeaderError):
    """Raised when leader ability execution fails.

    Provides specific factory methods for different types of ability
    execution failures with detailed context about the failure reason.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    @classmethod
    def for_invalid_target(
        cls, leader: BaseLeader, invalid_target: str, target_error: str
    ) -> LeaderAbilityError:
        """Create LeaderAbilityError for invalid ability target.

        Args:
            leader: The leader whose ability failed
            invalid_target: The invalid target that was specified
            target_error: Description of why the target is invalid

        Returns:
            LeaderAbilityError with target context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "invalid_target": invalid_target,
            "target_error": target_error,
        }
        return cls(
            f"{leader.get_name()} ability failed - invalid target '{invalid_target}': {target_error}",
            context=context,
        )

    @classmethod
    def for_insufficient_resources(
        cls,
        leader: BaseLeader,
        available_resources: dict[str, Any],
        required_resources: dict[str, Any],
    ) -> LeaderAbilityError:
        """Create LeaderAbilityError for insufficient resources.

        Args:
            leader: The leader whose ability failed
            available_resources: Resources currently available
            required_resources: Resources required for the ability

        Returns:
            LeaderAbilityError with resource context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "available_resources": available_resources,
            "required_resources": required_resources,
        }
        return cls(
            f"{leader.get_name()} ability failed - insufficient resources. "
            f"Required: {required_resources}, Available: {available_resources}",
            context=context,
        )

    @classmethod
    def for_timing_violation(
        cls, leader: BaseLeader, current_phase: str, required_phase: str
    ) -> LeaderAbilityError:
        """Create LeaderAbilityError for timing violation.

        Args:
            leader: The leader whose ability failed
            current_phase: The current game phase
            required_phase: The required game phase for the ability

        Returns:
            LeaderAbilityError with timing context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "current_phase": current_phase,
            "required_phase": required_phase,
        }
        return cls(
            f"{leader.get_name()} ability failed - timing violation. "
            f"Current phase: {current_phase}, Required phase: {required_phase}",
            context=context,
        )

    @classmethod
    def for_execution_failure(
        cls, leader: BaseLeader, execution_error: str
    ) -> LeaderAbilityError:
        """Create LeaderAbilityError for internal execution failure.

        Args:
            leader: The leader whose ability failed
            execution_error: Description of the execution error

        Returns:
            LeaderAbilityError with execution context
        """
        context = {
            "leader_name": leader.get_name(),
            "leader_type": leader.get_leader_type(),
            "execution_error": execution_error,
        }
        return cls(
            f"{leader.get_name()} ability execution failed: {execution_error}",
            context=context,
        )


# Leader Registry for faction-specific leader definitions


class LeaderRegistry:
    """Registry system for faction-specific leader definitions.

    Provides factory methods to create leaders for specific factions,
    leader lookup functionality, and validation of faction support.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 7.1, 7.2, 7.3, 7.4, 7.5
    """

    def __init__(self) -> None:
        """Initialize LeaderRegistry with faction definitions."""
        pass

    def create_faction_leaders(
        self, faction: Faction, player_id: str
    ) -> list[BaseLeader]:
        """Create all three leaders for a specific faction.

        Args:
            faction: The faction to create leaders for
            player_id: The ID of the player who will own these leaders

        Returns:
            List containing agent, commander, and hero leaders for the faction

        Raises:
            TypeError: If faction is not a Faction enum value
            ValueError: If player_id is empty or None

        LRR References:
        - Rule 51: LEADERS
        - Requirements 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        if not isinstance(faction, FactionEnum):
            raise TypeError("faction must be a Faction enum value")

        if not player_id or not player_id.strip():
            raise ValueError("player_id cannot be empty or None")

        # Create the three leaders for this faction
        agent = Agent(faction=faction, player_id=player_id)
        commander = Commander(faction=faction, player_id=player_id)
        hero = Hero(faction=faction, player_id=player_id)

        return [agent, commander, hero]

    def get_leader_definition(
        self, faction: Faction, leader_type: LeaderType
    ) -> dict[str, Any]:
        """Get leader definition information for a specific faction and type.

        Args:
            faction: The faction to get leader definition for
            leader_type: The type of leader (AGENT, COMMANDER, or HERO)

        Returns:
            Dictionary containing leader definition information

        Raises:
            TypeError: If faction is not a Faction enum value
            TypeError: If leader_type is not a LeaderType enum value

        LRR References:
        - Rule 51: LEADERS
        - Requirements 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        if not isinstance(faction, FactionEnum):
            raise TypeError("faction must be a Faction enum value")

        if not isinstance(leader_type, LeaderType):
            raise TypeError("leader_type must be a LeaderType enum value")

        # Placeholder implementation - actual definitions would come from compendium
        return {
            "name": f"{faction.value.title()} {leader_type.value.title()}",
            "unlock_conditions": []
            if leader_type == LeaderType.AGENT
            else ["Placeholder unlock condition"],
        }

    def validate_faction_support(self, faction: Faction) -> bool:
        """Validate that a faction is supported by the registry.

        Args:
            faction: The faction to validate support for

        Returns:
            True if faction is supported, False otherwise

        Raises:
            TypeError: If faction is not a Faction enum value

        LRR References:
        - Rule 51: LEADERS
        - Requirements 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        if not isinstance(faction, FactionEnum):
            raise TypeError("faction must be a Faction enum value")

        # For now, all factions in the enum are supported
        return True

    def get_supported_factions(self) -> list[Faction]:
        """Get list of all supported factions.

        Returns:
            List of all Faction enum values that are supported

        LRR References:
        - Rule 51: LEADERS
        - Requirements 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Import here to avoid circular imports
        from .constants import Faction as FactionEnum

        # Return all factions from the enum
        return list(FactionEnum)


# Leader Validation Framework


class LeaderAbilityValidator:
    """Comprehensive validation framework for leader ability execution.

    Provides validation for timing, game phase, resource availability, target legality,
    and other prerequisites for leader abilities.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    @staticmethod
    def validate_ability_execution(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate that a leader ability can be executed.

        Performs comprehensive validation including leader state, game phase,
        timing, resources, and targets.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for validation context
            **kwargs: Additional arguments for ability-specific validation

        Returns:
            None if validation passes, error message string if validation fails

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
        """
        # Validate leader state
        state_error = LeaderAbilityValidator._validate_leader_state(leader)
        if state_error:
            return state_error

        # Validate game phase and timing
        timing_error = LeaderAbilityValidator._validate_timing(
            leader, game_state, **kwargs
        )
        if timing_error:
            return timing_error

        # Validate resources if required
        resource_error = LeaderAbilityValidator._validate_resources(
            leader, game_state, **kwargs
        )
        if resource_error:
            return resource_error

        # Validate targets if specified
        target_error = LeaderAbilityValidator._validate_targets(
            leader, game_state, **kwargs
        )
        if target_error:
            return target_error

        return None

    @staticmethod
    def _validate_leader_state(leader: BaseLeader) -> str | None:
        """Validate that the leader is in a valid state to use abilities.

        Args:
            leader: The leader to validate

        Returns:
            None if valid, error message if invalid

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2
        """
        if not leader.can_use_ability():
            leader_type = leader.get_leader_type().value

            if isinstance(leader, Agent):
                if leader.lock_status != LeaderLockStatus.UNLOCKED:
                    return f"{leader_type.title()} {leader.get_name()} is not unlocked"
                if leader.ready_status != LeaderReadyStatus.READIED:
                    return f"{leader_type.title()} {leader.get_name()} is exhausted and cannot use abilities until readied"

            elif isinstance(leader, Commander):
                if leader.lock_status != LeaderLockStatus.UNLOCKED:
                    return f"{leader_type.title()} {leader.get_name()} is locked and cannot use abilities until unlocked"

            elif isinstance(leader, Hero):
                if leader.lock_status == LeaderLockStatus.LOCKED:
                    return f"{leader_type.title()} {leader.get_name()} is locked and cannot use abilities until unlocked"
                elif leader.lock_status == LeaderLockStatus.PURGED:
                    return f"{leader_type.title()} {leader.get_name()} has been purged and can no longer use abilities"

        return None

    @staticmethod
    def _validate_timing(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate timing and game phase for leader ability execution.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for phase validation
            **kwargs: Additional timing parameters

        Returns:
            None if timing is valid, error message if invalid

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.5
        """
        # Check if game phase allows leader abilities
        current_phase = getattr(game_state, "phase", None)

        # Always require a valid current phase for leader abilities
        if current_phase is None:
            return "Cannot determine current game phase for timing validation"

        # Get timing window requirement
        timing_window = kwargs.get("timing_window")

        # Import here to avoid circular imports

        # Validate phase-specific timing restrictions
        if timing_window and current_phase:
            phase_error = LeaderAbilityValidator._validate_phase_timing(
                current_phase, timing_window, leader
            )
            if phase_error:
                return phase_error

        # Validate sequence timing (e.g., before/after specific actions)
        sequence_error = LeaderAbilityValidator._validate_sequence_timing(
            leader, game_state, **kwargs
        )
        if sequence_error:
            return sequence_error

        return None

    @staticmethod
    def _validate_phase_timing(
        current_phase: Any, timing_window: str, leader: BaseLeader
    ) -> str | None:
        """Validate that the current game phase allows the leader ability.

        Args:
            current_phase: Current game phase
            timing_window: Required timing window for the ability
            leader: The leader whose ability is being validated

        Returns:
            None if phase timing is valid, error message if invalid
        """
        # Import here to avoid circular imports
        from .game_phase import GamePhase

        # Define valid phases for different timing windows
        valid_phases = {
            "action_phase": [GamePhase.ACTION],
            "status_phase": [GamePhase.STATUS],
            "strategy_phase": [GamePhase.STRATEGY],
            "agenda_phase": [GamePhase.AGENDA],
            "any_phase": [
                GamePhase.SETUP,
                GamePhase.STRATEGY,
                GamePhase.ACTION,
                GamePhase.STATUS,
                GamePhase.AGENDA,
            ],
            "tactical_action": [GamePhase.ACTION],
            "strategic_action": [GamePhase.ACTION],
        }

        allowed_phases = valid_phases.get(timing_window, [])
        if allowed_phases and current_phase not in allowed_phases:
            phase_names = [phase.value for phase in allowed_phases]
            return (
                f"{leader.get_leader_type().value.title()} {leader.get_name()} can only be used during "
                f"{', '.join(phase_names)} phase(s), but current phase is {current_phase.value}"
            )

        return None

    @staticmethod
    def _validate_sequence_timing(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate sequence-specific timing for leader abilities.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state
            **kwargs: Sequence timing parameters

        Returns:
            None if sequence timing is valid, error message if invalid

        Note:
            Sequence timing validation (before_action/after_action) is not yet implemented
            and requires additional game state tracking. Currently returns None (no validation).
        """
        # Validate timing relative to other actions
        before_action = kwargs.get("before_action")
        after_action = kwargs.get("after_action")

        if before_action:
            # TODO: Implement action sequence tracking
            pass

        if after_action:
            # TODO: Implement action sequence tracking
            pass

        return None

    @staticmethod
    def _validate_resources(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate resource availability for leader abilities.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for resource checking
            **kwargs: Resource requirement parameters

        Returns:
            None if resources are sufficient, error message if insufficient

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.3
        """
        # Get the player who owns this leader
        player = None
        for p in game_state.players:
            if p.id == leader.player_id:
                player = p
                break

        if not player:
            return f"Player {leader.player_id} not found for resource validation"

        # Validate trade goods cost
        trade_goods_cost = kwargs.get("trade_goods_cost", 0)
        if trade_goods_cost > 0:
            available_trade_goods = getattr(player, "trade_goods", 0)
            if available_trade_goods < trade_goods_cost:
                return (
                    f"{leader.get_leader_type().value.title()} {leader.get_name()} requires "
                    f"{trade_goods_cost} trade goods, but player only has {available_trade_goods}"
                )

        # Validate influence cost
        influence_cost = kwargs.get("influence_cost", 0)
        if influence_cost > 0:
            available_influence = getattr(player, "available_influence", 0)
            if available_influence < influence_cost:
                return (
                    f"{leader.get_leader_type().value.title()} {leader.get_name()} requires "
                    f"{influence_cost} influence, but player only has {available_influence}"
                )

        # Validate resource cost
        resource_cost = kwargs.get("resource_cost", 0)
        if resource_cost > 0:
            available_resources = getattr(player, "available_resources", 0)
            if available_resources < resource_cost:
                return (
                    f"{leader.get_leader_type().value.title()} {leader.get_name()} requires "
                    f"{resource_cost} resources, but player only has {available_resources}"
                )

        # Validate command token cost
        command_token_cost = kwargs.get("command_token_cost", 0)
        if command_token_cost > 0:
            available_tokens = getattr(player, "available_command_tokens", 0)
            if available_tokens < command_token_cost:
                return (
                    f"{leader.get_leader_type().value.title()} {leader.get_name()} requires "
                    f"{command_token_cost} command tokens, but player only has {available_tokens}"
                )

        return None

    @staticmethod
    def _validate_targets(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate target legality for leader abilities.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for target validation
            **kwargs: Target specification parameters

        Returns:
            None if targets are valid, error message if invalid

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.4
        """
        # Validate player targets
        if "target_player" in kwargs:
            target_player = kwargs["target_player"]
            target_error = LeaderAbilityValidator._validate_player_target(
                target_player, game_state, leader
            )
            if target_error:
                return target_error

        # Validate system targets
        if "target_system" in kwargs:
            target_system = kwargs["target_system"]
            system_error = LeaderAbilityValidator._validate_system_target(
                target_system, game_state, leader
            )
            if system_error:
                return system_error

        # Validate planet targets
        if "target_planet" in kwargs:
            target_planet = kwargs["target_planet"]
            planet_error = LeaderAbilityValidator._validate_planet_target(
                target_planet, game_state, leader
            )
            if planet_error:
                return planet_error

        # Validate unit targets
        if "target_units" in kwargs:
            target_units = kwargs["target_units"]
            unit_error = LeaderAbilityValidator._validate_unit_targets(
                target_units, game_state, leader
            )
            if unit_error:
                return unit_error

        return None

    @staticmethod
    def _validate_player_target(
        target_player: str, game_state: GameState, leader: BaseLeader
    ) -> str | None:
        """Validate that a player target is legal.

        Args:
            target_player: Player ID to validate
            game_state: Current game state
            leader: The leader whose ability is being validated

        Returns:
            None if target is valid, error message if invalid
        """
        # Check if target player exists
        target_exists = any(p.id == target_player for p in game_state.players)
        if not target_exists:
            return f"Target player {target_player} does not exist"

        # Check if targeting self is allowed (depends on ability)
        if target_player == leader.player_id:
            # Some abilities may not allow self-targeting
            # This would be ability-specific validation
            pass

        return None

    @staticmethod
    def _validate_system_target(
        target_system: str, game_state: GameState, leader: BaseLeader
    ) -> str | None:
        """Validate that a system target is legal.

        Args:
            target_system: System identifier to validate
            game_state: Current game state
            leader: The leader whose ability is being validated

        Returns:
            None if target is valid, error message if invalid
        """
        # Check if system exists in the galaxy
        # This would require access to the galaxy/map structure
        # For now, assume basic validation
        if target_system == "":  # Explicitly check for empty string
            return "System target cannot be empty"

        return None

    @staticmethod
    def _validate_planet_target(
        target_planet: str, game_state: GameState, leader: BaseLeader
    ) -> str | None:
        """Validate that a planet target is legal.

        Args:
            target_planet: Planet name to validate
            game_state: Current game state
            leader: The leader whose ability is being validated

        Returns:
            None if target is valid, error message if invalid
        """
        # Check if planet exists
        # This would require access to the galaxy/planet structure
        # For now, assume basic validation
        if target_planet == "":  # Explicitly check for empty string
            return "Planet target cannot be empty"

        return None

    @staticmethod
    def _validate_unit_targets(
        target_units: list[str], game_state: GameState, leader: BaseLeader
    ) -> str | None:
        """Validate that unit targets are legal.

        Args:
            target_units: List of unit identifiers to validate
            game_state: Current game state
            leader: The leader whose ability is being validated

        Returns:
            None if targets are valid, error message if invalid
        """
        if len(target_units) == 0:  # Explicitly check for empty list
            return "Unit targets list cannot be empty when specified"

        # Validate each unit target
        for unit in target_units:
            if not unit or not unit.strip():
                return "Unit target cannot be empty"

        return None

    @staticmethod
    def validate_unlock_conditions(
        leader: BaseLeader, game_state: GameState
    ) -> str | None:
        """Validate that a leader can be unlocked.

        Performs comprehensive validation for unlock attempts including
        leader state, unlock conditions, and game state requirements.

        Args:
            leader: The leader to validate for unlocking
            game_state: Current game state for validation context

        Returns:
            None if unlock is valid, error message string if invalid

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.5
        """
        # Agents don't need to be unlocked - they start unlocked
        if isinstance(leader, Agent):
            return "Agents do not need to be unlocked - they start unlocked"

        # Check if leader is in a state that can be unlocked
        if leader.lock_status == LeaderLockStatus.UNLOCKED:
            return f"{leader.get_leader_type().value.title()} {leader.get_name()} is already unlocked"

        if leader.lock_status == LeaderLockStatus.PURGED:
            return f"{leader.get_leader_type().value.title()} {leader.get_name()} has been purged and cannot be unlocked"

        # Check if unlock conditions are met
        if not leader.check_unlock_conditions(game_state):
            conditions = leader.get_unlock_conditions()
            conditions_str = (
                ", ".join(conditions) if conditions else "unknown conditions"
            )
            return (
                f"Unlock conditions not met for {leader.get_name()}: {conditions_str}"
            )

        return None

    @staticmethod
    def validate_state_transition(
        leader: BaseLeader, from_state: str, to_state: str, operation: str
    ) -> str | None:
        """Validate that a leader state transition is legal.

        Args:
            leader: The leader whose state is being changed
            from_state: The current state description
            to_state: The target state description
            operation: The operation being performed

        Returns:
            None if transition is valid, error message if invalid

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2
        """
        leader_type = leader.get_leader_type().value.title()

        # Validate agent state transitions
        if isinstance(leader, Agent):
            if operation == "exhaust":
                if leader.ready_status != LeaderReadyStatus.READIED:
                    return f"Cannot exhaust {leader_type} {leader.get_name()} - not in readied state"
            elif operation == "ready":
                if leader.ready_status != LeaderReadyStatus.EXHAUSTED:
                    return f"Cannot ready {leader_type} {leader.get_name()} - not in exhausted state"

        # Validate commander state transitions
        elif isinstance(leader, Commander):
            if operation == "unlock":
                if leader.lock_status != LeaderLockStatus.LOCKED:
                    return f"Cannot unlock {leader_type} {leader.get_name()} - not in locked state"

        # Validate hero state transitions
        elif isinstance(leader, Hero):
            if operation == "unlock":
                if leader.lock_status == LeaderLockStatus.PURGED:
                    return f"Cannot unlock {leader_type} {leader.get_name()} - hero has been purged"
                if leader.lock_status == LeaderLockStatus.UNLOCKED:
                    return f"Cannot unlock {leader_type} {leader.get_name()} - already unlocked"
            elif operation == "purge":
                # Heroes can be purged from any non-purged state
                if leader.lock_status == LeaderLockStatus.PURGED:
                    return f"Cannot purge {leader_type} {leader.get_name()} - already purged"

        return None

    @staticmethod
    def validate_comprehensive_prerequisites(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> list[str]:
        """Perform comprehensive validation and return all validation errors.

        Unlike other validation methods that return the first error found,
        this method collects all validation errors to provide complete feedback.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for validation context
            **kwargs: Additional validation parameters

        Returns:
            List of all validation error messages (empty if all validation passes)

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
        """
        errors: list[str] = []

        # Collect all validation errors
        state_error = LeaderAbilityValidator._validate_leader_state(leader)
        if state_error:
            errors.append(state_error)

        timing_error = LeaderAbilityValidator._validate_timing(
            leader, game_state, **kwargs
        )
        if timing_error:
            errors.append(timing_error)

        resource_error = LeaderAbilityValidator._validate_resources(
            leader, game_state, **kwargs
        )
        if resource_error:
            errors.append(resource_error)

        target_error = LeaderAbilityValidator._validate_targets(
            leader, game_state, **kwargs
        )
        if target_error:
            errors.append(target_error)

        return errors

    @staticmethod
    def validate_edge_cases(
        leader: BaseLeader, game_state: GameState, **kwargs: Any
    ) -> str | None:
        """Validate edge cases and unusual scenarios for leader abilities.

        Args:
            leader: The leader whose ability is being validated
            game_state: Current game state for validation context
            **kwargs: Additional validation parameters

        Returns:
            None if validation passes, error message if validation fails

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
        """
        # Check for null/empty parameters
        if not leader:
            return "Leader cannot be None"

        if not game_state:
            return "Game state cannot be None"

        # Check for invalid leader types
        if not hasattr(leader, "get_leader_type"):
            return "Invalid leader object - missing get_leader_type method"

        try:
            leader_type = leader.get_leader_type()
            if leader_type not in [
                LeaderType.AGENT,
                LeaderType.COMMANDER,
                LeaderType.HERO,
            ]:
                return f"Invalid leader type: {leader_type}"
        except Exception:
            return "Invalid leader object - missing get_leader_type method"

        # Check for invalid player ownership
        if not hasattr(leader, "player_id") or not leader.player_id:
            return "Leader must have a valid player_id"

        # Validate player exists in game state
        if not hasattr(game_state, "players"):
            return "Game state must have players list"

        if not game_state.players:
            return f"Leader's player {leader.player_id} not found in game state"

        player_exists = any(
            p.id == leader.player_id for p in game_state.players if hasattr(p, "id")
        )
        if not player_exists:
            return f"Leader's player {leader.player_id} not found in game state"

        # Check for circular references or invalid state combinations
        if isinstance(leader, Agent):
            if leader.lock_status != LeaderLockStatus.UNLOCKED:
                return f"Agent {leader.get_name()} has invalid lock status: {leader.lock_status}"
            if leader.ready_status not in [
                LeaderReadyStatus.READIED,
                LeaderReadyStatus.EXHAUSTED,
            ]:
                return f"Agent {leader.get_name()} has invalid ready status: {leader.ready_status}"

        elif isinstance(leader, (Commander, Hero)):
            if hasattr(leader, "ready_status") and leader.ready_status is not None:
                return f"{leader.get_leader_type().value.title()} {leader.get_name()} should not have ready_status"

        return None


# Leader Manager for coordinating leader operations


class LeaderManager:
    """Manager class for coordinating leader operations.

    Handles leader lifecycle management, unlock condition checking, ability execution,
    and validation. Provides a centralized interface for all leader-related operations.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 9.5
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize LeaderManager with game state.

        Args:
            game_state: The game state to manage leaders for

        Raises:
            ValueError: If game_state is None
        """
        if game_state is None:
            raise ValueError("game_state cannot be None")
        self.game_state = game_state

    def _get_player(self, player_id: str) -> Player:
        """Get a player from the game state by ID.

        Args:
            player_id: The ID of the player to retrieve

        Returns:
            The player with the specified ID

        Raises:
            LeaderNotFoundError: If player doesn't exist
        """
        if not player_id or not player_id.strip():
            raise LeaderNotFoundError("player_id cannot be empty or None")

        player_id = player_id.strip()
        for player in self.game_state.players:
            if player.id == player_id:
                return player
        raise LeaderNotFoundError(f"Player {player_id} not found")

    def check_unlock_conditions(self, player_id: str) -> None:
        """Check and process unlock conditions for all player leaders.

        Iterates through all leaders for the specified player and checks if their
        unlock conditions are met. If conditions are met, automatically unlocks
        the leader.

        Args:
            player_id: The ID of the player whose leaders to check

        Raises:
            LeaderNotFoundError: If player doesn't exist

        LRR References:
        - Rule 51: LEADERS
        - Requirements 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 9.5
        """
        player = self._get_player(player_id)

        for leader in player.leader_sheet.get_all_leaders():
            if leader.lock_status == LeaderLockStatus.LOCKED:
                if leader.check_unlock_conditions(self.game_state):
                    leader.unlock()

    def ready_agents(self, player_id: str) -> None:
        """Ready all exhausted agents during status phase.

        Iterates through all leaders for the specified player and readies any
        exhausted agents. This is typically called during the status phase
        "Ready Cards" step.

        Args:
            player_id: The ID of the player whose agents to ready

        Raises:
            LeaderNotFoundError: If player doesn't exist

        LRR References:
        - Rule 51: LEADERS
        - Requirements 2.3, 8.4
        """
        player = self._get_player(player_id)

        for leader in player.leader_sheet.get_all_leaders():
            if isinstance(leader, Agent):
                if leader.ready_status == LeaderReadyStatus.EXHAUSTED:
                    leader.ready()

    def execute_leader_ability(
        self, player_id: str, leader_name: str, **kwargs: Any
    ) -> LeaderAbilityResult:
        """Execute a leader's ability with comprehensive validation.

        Finds the specified leader and executes their ability if they pass all
        validation checks including state, timing, resources, and targets.
        Handles post-ability state changes (exhausting agents, purging heroes).

        Args:
            player_id: The ID of the player whose leader to use
            leader_name: The name of the leader whose ability to execute
            **kwargs: Additional arguments to pass to the leader's ability

        Returns:
            LeaderAbilityResult with success status, effects, and any error messages

        Raises:
            LeaderNotFoundError: If player doesn't exist

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
        """
        player = self._get_player(player_id)

        # Find the leader by name
        leader = player.leader_sheet.get_leader_by_name(leader_name)

        if not leader:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Leader {leader_name} not found",
            )

        # Comprehensive validation using the validation framework
        validation_error = LeaderAbilityValidator.validate_ability_execution(
            leader, self.game_state, **kwargs
        )

        if validation_error:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=validation_error,
            )

        # Execute the ability
        result = leader.execute_ability(self.game_state, **kwargs)

        # Handle post-ability state changes if ability was successful
        if result.success:
            if isinstance(leader, Agent):
                leader.exhaust()
            elif isinstance(leader, Hero):
                leader.purge()

        return result

    def validate_leader_ability(
        self, player_id: str, leader_name: str, **kwargs: Any
    ) -> str | None:
        """Validate a leader ability without executing it.

        Performs the same validation as execute_leader_ability but without
        actually executing the ability or changing any state.

        Args:
            player_id: The ID of the player whose leader to validate
            leader_name: The name of the leader whose ability to validate
            **kwargs: Additional arguments for validation

        Returns:
            None if validation passes, error message string if validation fails

        Raises:
            LeaderNotFoundError: If player doesn't exist

        LRR References:
        - Rule 51: LEADERS
        - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
        """
        player = self._get_player(player_id)

        # Find the leader by name
        leader = player.leader_sheet.get_leader_by_name(leader_name)

        if not leader:
            return f"Leader {leader_name} not found"

        # Use the validation framework
        return LeaderAbilityValidator.validate_ability_execution(
            leader, self.game_state, **kwargs
        )
