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
    FLAGSHIP = "flagship"
    INFANTRY = "infantry"
    MECH = "mech"
    PDS = "pds"
    SPACE_DOCK = "space_dock"
    WAR_SUN = "war_sun"


class LocationType(Enum):
    """Enumeration of unit location types."""

    SPACE = "space"
    PLANET = "planet"


class EventType(Enum):
    """Enumeration of game event types."""

    UNIT_MOVED = "unit_moved"
    COMBAT_STARTED = "combat_started"
    PHASE_CHANGED = "phase_changed"


class CircuitBreakerState(Enum):
    """Enumeration of circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class GameConstants:
    """Game constants and configuration."""

    # Starting command tokens per player (TI4 rules 20.1)
    # "Each player begins the game with eight tokens on their command sheet"
    STARTING_COMMAND_TOKENS = 8
    STARTING_TACTIC_TOKENS = 3  # For tactical actions (activating systems)
    STARTING_FLEET_TOKENS = 3  # For fleet supply (max separate fleets allowed)
    STARTING_STRATEGY_TOKENS = 2  # For secondary abilities of strategy cards

    # Player limits
    MAX_PLAYERS = 6
    MIN_PLAYERS = 3  # TI4 requires at least 3 players

    # Strategy cards
    STRATEGY_CARD_COUNT = 8

    # Combat
    DEFAULT_COMBAT_DICE_SIDES = 10

    # Starting values
    STARTING_RESOURCES = 0
    STARTING_INFLUENCE = 0

    # Movement
    DEFAULT_MOVEMENT_RANGE = 1

    # Capacity costs
    FIGHTER_CAPACITY_COST = 1
    INFANTRY_CAPACITY_COST = 1
    MECH_CAPACITY_COST = 1

    # Unit type sets for common operations
    GROUND_FORCE_TYPES = frozenset({UnitType.INFANTRY, UnitType.MECH})
    SHIP_TYPES = frozenset(
        {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.CRUISER_II,
            UnitType.DREADNOUGHT,
            UnitType.DESTROYER,
            UnitType.FIGHTER,
            UnitType.FLAGSHIP,
            UnitType.WAR_SUN,
        }
    )
    # Optional: for rules that treat fighters differently (e.g., movement blocking)
    NON_FIGHTER_SHIP_TYPES = SHIP_TYPES - frozenset({UnitType.FIGHTER})


class Technology(Enum):
    """Enumeration of TI4 technologies."""

    # Movement technologies
    GRAVITY_DRIVE = "gravity_drive"
    FLEET_LOGISTICS = "fleet_logistics"
    LIGHT_WAVE_DEFLECTOR = "light_wave_deflector"
    ANTIMASS_DEFLECTORS = "antimass_deflectors"

    # Unit upgrade technologies
    CRUISER_II = "cruiser_ii"
    DREADNOUGHT_II = "dreadnought_ii"
    CARRIER_II = "carrier_ii"
    DESTROYER_II = "destroyer_ii"
    FIGHTER_II = "fighter_ii"

    # Other technologies
    PLASMA_SCORING = "plasma_scoring"

    # Faction-specific technologies (manually confirmed)
    # Sol Federation faction technologies
    SPEC_OPS_II = (
        "spec_ops_ii"  # Confirmed Sol faction tech - unit upgrade, 2x green prereq
    )

    # Hacan Emirates faction technologies
    QUANTUM_DATAHUB_NODE = "quantum_datahub_node"  # Confirmed Hacan faction tech - yellow, 3x yellow prereq


class TechnologyConstants:
    """Technology-related constants (deprecated - use Technology enum instead)."""

    # Deprecated: Use Technology enum instead
    GRAVITY_DRIVE = Technology.GRAVITY_DRIVE.value
    FLEET_LOGISTICS = Technology.FLEET_LOGISTICS.value
    LIGHT_WAVE_DEFLECTOR = Technology.LIGHT_WAVE_DEFLECTOR.value

    # Unit upgrade technologies
    CRUISER_II_TECH = Technology.CRUISER_II.value
    DREADNOUGHT_II_TECH = Technology.DREADNOUGHT_II.value
    CARRIER_II_TECH = Technology.CARRIER_II.value
    DESTROYER_II_TECH = Technology.DESTROYER_II.value
    FIGHTER_II_TECH = Technology.FIGHTER_II.value


class Faction(Enum):
    """Enumeration of TI4 factions."""

    SOL = "sol"
    HACAN = "hacan"
    XXCHA = "xxcha"
    JORD = "jord"
    YSSARIL = "yssaril"
    NAALU = "naalu"
    BARONY = "barony"
    SAAR = "saar"
    MUAAT = "muaat"
    ARBOREC = "arborec"
    L1Z1X = "l1z1x"
    WINNU = "winnu"


class FactionConstants:
    """Faction-related constants (deprecated - use Faction enum instead)."""

    # Deprecated: Use Faction enum instead
    SOL = Faction.SOL.value
    HACAN = Faction.HACAN.value
    XXCHA = Faction.XXCHA.value
    JORD = Faction.JORD.value


class EventConstants:
    """Event type constants."""

    # Deprecated: Use EventType enum instead
    UNIT_MOVED = EventType.UNIT_MOVED.value
    COMBAT_STARTED = EventType.COMBAT_STARTED.value
    PHASE_CHANGED = EventType.PHASE_CHANGED.value


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
    """Circuit breaker state constants."""

    # Deprecated: Use CircuitBreakerState enum instead
    STATE_CLOSED = CircuitBreakerState.CLOSED.value
    STATE_OPEN = CircuitBreakerState.OPEN.value
    STATE_HALF_OPEN = CircuitBreakerState.HALF_OPEN.value


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
