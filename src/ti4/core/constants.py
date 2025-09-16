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
    MIN_PLAYERS = 2

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
