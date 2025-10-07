"""Constants and configuration for TI4 game framework."""

from dataclasses import dataclass
from enum import Enum


class UnitType(Enum):
    """Enumeration of unit types."""

    CARRIER = "carrier"
    CRUISER = "cruiser"
    CRUISER_II = "cruiser_ii"
    DREADNOUGHT = "dreadnought"
    DREADNOUGHT_II = "dreadnought_ii"
    DESTROYER = "destroyer"
    DESTROYER_II = "destroyer_ii"
    FIGHTER = "fighter"
    FIGHTER_II = "fighter_ii"
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


class WormholeType(Enum):
    """Enumeration of wormhole types as defined in Rule 101."""

    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"
    DELTA = "delta"


class AnomalyType(Enum):
    """Enumeration of anomaly types as defined in Rule 9."""

    ASTEROID_FIELD = "asteroid_field"
    NEBULA = "nebula"
    SUPERNOVA = "supernova"
    GRAVITY_RIFT = "gravity_rift"


class CircuitBreakerState(Enum):
    """Enumeration of circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class AgendaType(Enum):
    """Enumeration of agenda card types."""

    LAW = "law"
    DIRECTIVE = "directive"


class VotingOutcomes:
    """Constants for agenda card voting outcomes."""

    FOR_AGAINST: tuple[str, ...] = ("For", "Against")
    ELECT_PLAYER: tuple[str, ...] = ("Elect Player",)
    ELECT_PLANET_CULTURAL: tuple[str, ...] = ("Elect Cultural Planet",)
    ELECT_PLANET_INDUSTRIAL: tuple[str, ...] = ("Elect Industrial Planet",)
    ELECT_PLANET_HAZARDOUS: tuple[str, ...] = ("Elect Hazardous Planet",)
    ELECT_SECRET_OBJECTIVE: tuple[str, ...] = ("Elect Scored Secret Objective",)


@dataclass
class AgendaCardMetadata:
    """Metadata structure for agenda cards."""

    name: str
    agenda_type: AgendaType
    outcomes: list[str]
    expansion: str = "Base"


class AgendaCardHelpers:
    """Helper methods for agenda card identification and validation."""

    @staticmethod
    def is_law_card(agenda_type: AgendaType) -> bool:
        """Check if the agenda type represents a law card."""
        return agenda_type == AgendaType.LAW

    @staticmethod
    def is_directive_card(agenda_type: AgendaType) -> bool:
        """Check if the agenda type represents a directive card."""
        return agenda_type == AgendaType.DIRECTIVE

    @staticmethod
    def is_valid_outcome(outcome: str, valid_outcomes: list[str]) -> bool:
        """Check if an outcome is valid for the given list of outcomes."""
        return outcome in valid_outcomes


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

    # Prophecy of Kings technologies
    DARK_ENERGY_TAP = (
        "dark_energy_tap"  # Confirmed: Blue tech, no prerequisites, Prophecy of Kings
    )
    AI_DEVELOPMENT_ALGORITHM = "ai_development_algorithm"  # Confirmed: Yellow tech, no prerequisites, Prophecy of Kings


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


class Expansion(Enum):
    """Enumeration of TI4 expansions for technology framework."""

    BASE = "base"
    PROPHECY_OF_KINGS = "prophecy_of_kings"
    CODEX_I = "codex_i"
    CODEX_II = "codex_ii"
    CODEX_III = "codex_iii"


class AbilityTrigger(Enum):
    """Enumeration of ability triggers for technology framework."""

    ACTION = "action"
    AFTER_ACTIVATE_SYSTEM = "after_activate_system"
    AFTER_TACTICAL_ACTION = "after_tactical_action"
    WHEN_RESEARCH_TECHNOLOGY = "when_research_technology"
    START_OF_TURN = "start_of_turn"
    END_OF_TURN = "end_of_turn"
    # Additional triggers from TI4 ability compendium analysis
    WHEN_RETREAT_DECLARED = "when_retreat_declared"
    BEFORE_COMBAT = "before_combat"
    AFTER_COMBAT = "after_combat"
    WHEN_PRODUCING_UNITS = "when_producing_units"
    START_OF_PHASE = "start_of_phase"
    END_OF_PHASE = "end_of_phase"


class AbilityEffectType(Enum):
    """Enumeration of ability effect types for technology framework."""

    EXPLORE_FRONTIER_TOKEN = "explore_frontier_token"
    ALLOW_RETREAT_TO_EMPTY_ADJACENT = "allow_retreat_to_empty_adjacent"
    MODIFY_UNIT_STATS = "modify_unit_stats"
    GAIN_TRADE_GOODS = "gain_trade_goods"
    # Additional effect types from TI4 ability compendium analysis
    GAIN_RESOURCES = "gain_resources"
    GAIN_INFLUENCE = "gain_influence"
    GAIN_COMMAND_TOKENS = "gain_command_tokens"
    MODIFY_MOVEMENT = "modify_movement"
    MODIFY_COMBAT_VALUE = "modify_combat_value"
    MODIFY_CAPACITY = "modify_capacity"
    DRAW_ACTION_CARDS = "draw_action_cards"
    RESEARCH_TECHNOLOGY = "research_technology"


class AbilityCondition(Enum):
    """Enumeration of ability conditions for technology framework."""

    HAS_SHIPS_IN_SYSTEM = "has_ships_in_system"
    CONTROL_PLANET = "control_planet"
    SYSTEM_CONTAINS_FRONTIER = "system_contains_frontier"
    # Additional conditions from TI4 ability compendium analysis
    HAS_GROUND_FORCES_ON_PLANET = "has_ground_forces_on_planet"
    SYSTEM_CONTAINS_WORMHOLE = "system_contains_wormhole"
    ADJACENT_TO_MECATOL_REX = "adjacent_to_mecatol_rex"
    DURING_COMBAT = "during_combat"
    DURING_TACTICAL_ACTION = "during_tactical_action"
    HAS_TECHNOLOGY_OF_COLOR = "has_technology_of_color"
    CONTROLS_LEGENDARY_PLANET = "controls_legendary_planet"


class UnitStatModification(Enum):
    """Enumeration of unit stat modification types for technology framework."""

    # Fundamental unit properties
    COST = "cost"
    COMBAT_VALUE = "combat_value"
    COMBAT_DICE = "combat_dice"
    MOVEMENT = "movement"
    CAPACITY = "capacity"
    PRODUCTION = "production"

    # Unit abilities
    SUSTAIN_DAMAGE = "sustain_damage"
    ANTI_FIGHTER_BARRAGE = "anti_fighter_barrage"
    BOMBARDMENT = "bombardment"
    BOMBARDMENT_VALUE = "bombardment_value"
    BOMBARDMENT_DICE = "bombardment_dice"
    DEPLOY = "deploy"
    PLANETARY_SHIELD = "planetary_shield"
    SPACE_CANNON = "space_cannon"
    SPACE_CANNON_VALUE = "space_cannon_value"
    SPACE_CANNON_DICE = "space_cannon_dice"
    HAS_PRODUCTION = "has_production"


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


class SystemConstants:
    """Constants for game systems."""

    # Special system identifiers
    MECATOL_REX_ID = "18"


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
