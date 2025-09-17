"""Constants and configuration for TI4 game framework."""

from enum import Enum


class UnitType(Enum):
    """Enumeration of unit types."""

    CARRIER = "carrier"
    CRUISER = "cruiser"
    CRUISER_II = "cruiser_ii"
    DREADNOUGHT = "dreadnought"
    DESTROYER = "destroyer"
    FIGHTER = "fighter"
    INFANTRY = "infantry"
    MECH = "mech"
    PDS = "pds"
    SPACE_DOCK = "space_dock"
    WAR_SUN = "war_sun"


class GameConstants:
    """Game constants and configuration."""

    # Starting command tokens per player (TI4 rules 20.1)
    # "Each player begins the game with eight tokens on their command sheet"
    STARTING_TACTIC_TOKENS = 3  # For tactical actions (activating systems)
    STARTING_FLEET_TOKENS = 3  # For fleet supply (max separate fleets allowed)
    STARTING_STRATEGY_TOKENS = 2  # For secondary abilities of strategy cards

    # Total starting tokens = 8 (3 + 3 + 2)

    # Maximum number of players
    MAX_PLAYERS = 6
    MIN_PLAYERS = 3  # TI4 requires at least 3 players

    # Strategy cards
    STRATEGY_CARD_COUNT = 8

    # Combat
    DEFAULT_COMBAT_DICE_SIDES = 10

    # Resources
    STARTING_RESOURCES = 0
    STARTING_INFLUENCE = 0

    # Movement
    DEFAULT_MOVEMENT_RANGE = 1

    # Fleet capacity
    FIGHTER_CAPACITY_COST = 1
    INFANTRY_CAPACITY_COST = 1


class TechnologyConstants:
    """Technology-related constants."""

    # Common technologies that affect movement
    GRAVITY_DRIVE = "gravity_drive"
    FLEET_LOGISTICS = "fleet_logistics"
    LIGHT_WAVE_DEFLECTOR = "light_wave_deflector"

    # Unit upgrade technologies
    CRUISER_II_TECH = "cruiser_ii"
    DREADNOUGHT_II_TECH = "dreadnought_ii"
    CARRIER_II_TECH = "carrier_ii"
    DESTROYER_II_TECH = "destroyer_ii"
    FIGHTER_II_TECH = "fighter_ii"


class FactionConstants:
    """Faction-related constants."""

    # Example factions (would be expanded)
    SOL = "sol"
    HACAN = "hacan"
    XXCHA = "xxcha"
    JORD = "jord"


class EventConstants:
    """Event type constants for the event system."""

    UNIT_MOVED = "unit_moved"
    COMBAT_STARTED = "combat_started"
    PHASE_CHANGED = "phase_changed"


class PerformanceConstants:
    """Performance and resource management constants."""

    # Cache sizes
    DEFAULT_CACHE_SIZE = 1000
    DEFAULT_MAX_STATES = 100
    DEFAULT_MAX_CONCURRENT_GAMES = 100

    # Timeouts and delays
    CIRCUIT_BREAKER_TIMEOUT = 60.0  # seconds
    DEFAULT_RETRY_DELAY = 1.0  # seconds
    OPERATION_SLEEP_DELAY = 0.01  # seconds
    INACTIVE_GAME_THRESHOLD = 3600  # 1 hour in seconds
    OLD_STATE_THRESHOLD = 3600  # 1 hour in seconds

    # Retry and failure thresholds
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_FAILURE_THRESHOLD = 5
    MAX_OPERATION_HISTORY = 1000

    # Thread pool settings
    DEFAULT_MAX_WORKERS = 10
    THREAD_NAME_PREFIX = "ti4-game"


class ValidationConstants:
    """Constants for validation logic."""

    # Collection length checks
    EMPTY_COLLECTION_LENGTH = 0
    POSITIVE_NUMBER_THRESHOLD = 0


class CircuitBreakerConstants:
    """Constants for circuit breaker pattern."""

    STATE_CLOSED = "closed"
    STATE_OPEN = "open"
    STATE_HALF_OPEN = "half-open"


class GameStateConstants:
    """Constants for game state management."""

    # Default starting values
    DEFAULT_CURRENT_PLAYER_INDEX = 0
    DEFAULT_ROUND_NUMBER = 1

    # Token counts (from TI4 rules 20.1)
    DEFAULT_TACTIC_TOKENS = 3
    DEFAULT_FLEET_TOKENS = 3
    DEFAULT_STRATEGY_TOKENS = 2

    # Resource starting values
    DEFAULT_RESOURCES = 0
    DEFAULT_INFLUENCE = 0
