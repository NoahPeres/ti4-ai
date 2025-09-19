"""Tests for Rule 17: CAPTURE mechanics.

This module tests the capture system according to TI4 LRR Rule 17.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 17 Sub-rules tested:
- 17.1: Non-fighter ship/mech capture to faction sheet
- 17.2: Return conditions for captured ships/mechs
- 17.3: Fighter/infantry capture as tokens
- 17.4: Fighter/infantry return rules
- 17.5: Production restriction for captured units
- 17.6: Blockade capture restriction
"""

from src.ti4.core.constants import UnitType
from src.ti4.core.unit import Unit


class TestRule17CaptureBasics:
    """Test basic capture mechanics (Rule 17.0)."""

    def test_capture_system_exists(self) -> None:
        """Test that capture system can be imported and instantiated.

        This is the first RED test - it will fail until we create the capture system.

        LRR Reference: Rule 17.0 - Core capture concept
        """
        # This will fail initially - RED phase
        from src.ti4.core.capture import CaptureManager

        capture_manager = CaptureManager()
        assert capture_manager is not None


class TestRule17NonFighterCapture:
    """Test capture of non-fighter ships and mechs (Rule 17.1)."""

    def test_capture_cruiser_to_faction_sheet(self) -> None:
        """Test capturing a cruiser places it on the capturing player's faction sheet.

        LRR Reference: Rule 17.1 - "If a player captures a non-fighter ship or mech,
        they place it on their faction sheet."
        """
        from src.ti4.core.capture import CaptureManager

        # Create a cruiser owned by player1
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Create capture manager
        capture_manager = CaptureManager()

        # Player2 captures the cruiser
        capture_manager.capture_unit(cruiser, capturing_player="player2")

        # Verify cruiser is on player2's faction sheet
        captured_units = capture_manager.get_faction_sheet_units("player2")
        assert cruiser in captured_units

        # Verify cruiser is no longer available to player1
        assert not capture_manager.is_unit_available_to_owner(cruiser)

    def test_capture_mech_to_faction_sheet(self) -> None:
        """Test capturing a mech places it on the capturing player's faction sheet.

        LRR Reference: Rule 17.1 - Non-fighter ships and mechs go to faction sheet
        """
        from src.ti4.core.capture import CaptureManager

        # Create a mech owned by player1
        mech = Unit(unit_type=UnitType.MECH, owner="player1")

        # Create capture manager
        capture_manager = CaptureManager()

        # Player2 captures the mech
        capture_manager.capture_unit(mech, capturing_player="player2")

        # Verify mech is on player2's faction sheet
        captured_units = capture_manager.get_faction_sheet_units("player2")
        assert mech in captured_units


class TestRule17FighterInfantryCapture:
    """Test capture of fighters and infantry (Rule 17.3)."""

    def test_capture_fighter_becomes_token(self) -> None:
        """Test capturing a fighter creates a token on faction sheet.

        LRR Reference: Rule 17.3 - "If a player captures a fighter or infantry,
        it is placed in its reinforcements instead of on the capturing player's
        faction sheet; the capturing player places a fighter or infantry token
        from the supply on their faction sheet instead."
        """
        from src.ti4.core.capture import CaptureManager

        # Create a fighter owned by player1
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Create capture manager
        capture_manager = CaptureManager()

        # Player2 captures the fighter
        capture_manager.capture_unit(fighter, capturing_player="player2")

        # Verify fighter is NOT on player2's faction sheet (goes to reinforcements)
        captured_units = capture_manager.get_faction_sheet_units("player2")
        assert fighter not in captured_units

        # Verify player2 has a fighter token on their faction sheet
        fighter_tokens = capture_manager.get_faction_sheet_tokens(
            "player2", UnitType.FIGHTER
        )
        assert fighter_tokens == 1

    def test_capture_infantry_becomes_token(self) -> None:
        """Test capturing infantry creates a token on faction sheet.

        LRR Reference: Rule 17.3 - Infantry capture creates tokens like fighters
        """
        from src.ti4.core.capture import CaptureManager

        # Create infantry owned by player1
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Create capture manager
        capture_manager = CaptureManager()

        # Player2 captures the infantry
        capture_manager.capture_unit(infantry, capturing_player="player2")

        # Verify infantry is NOT on player2's faction sheet
        captured_units = capture_manager.get_faction_sheet_units("player2")
        assert infantry not in captured_units

        # Verify player2 has an infantry token on their faction sheet
        infantry_tokens = capture_manager.get_faction_sheet_tokens(
            "player2", UnitType.INFANTRY
        )
        assert infantry_tokens == 1


class TestRule17UnitReturn:
    """Test return conditions for captured units (Rule 17.2, 17.4)."""

    def test_return_captured_ship_to_reinforcements(self) -> None:
        """Test returning a captured ship places it in original owner's reinforcements.

        LRR Reference: Rule 17.1 - "When such a unit is returned, it is placed
        into the reinforcements of the original owner."
        """
        from src.ti4.core.capture import CaptureManager

        # Create and capture a cruiser
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        capture_manager = CaptureManager()
        capture_manager.capture_unit(cruiser, capturing_player="player2")

        # Return the captured cruiser
        capture_manager.return_unit(cruiser, returning_player="player2")

        # Verify cruiser is no longer on player2's faction sheet
        captured_units = capture_manager.get_faction_sheet_units("player2")
        assert cruiser not in captured_units

        # Verify cruiser is available to original owner again
        assert capture_manager.is_unit_available_to_owner(cruiser)


class TestRule17ProductionRestriction:
    """Test production restriction for captured units (Rule 17.5)."""

    def test_captured_unit_cannot_be_produced(self) -> None:
        """Test that captured units cannot be produced by original owner.

        LRR Reference: Rule 17.5 - "While a unit is captured, it cannot be
        produced or placed by its original owner until it is returned."
        """
        from src.ti4.core.capture import CaptureManager

        # Create and capture a cruiser
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        capture_manager = CaptureManager()
        capture_manager.capture_unit(cruiser, capturing_player="player2")

        # Verify unit is not available for production by original owner
        assert not capture_manager.can_produce_unit(cruiser, "player1")

        # Verify unit can still be produced by other players (different instance)
        other_cruiser = Unit(unit_type=UnitType.CRUISER, owner="player3")
        assert capture_manager.can_produce_unit(other_cruiser, "player3")

    def test_returned_unit_can_be_produced_again(self) -> None:
        """Test that returned units can be produced by original owner again.

        LRR Reference: Rule 17.5 - Units can be produced again after return
        """
        from src.ti4.core.capture import CaptureManager

        # Create, capture, and return a cruiser
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        capture_manager = CaptureManager()
        capture_manager.capture_unit(cruiser, capturing_player="player2")
        capture_manager.return_unit(cruiser, returning_player="player2")

        # Verify unit can be produced by original owner again
        assert capture_manager.can_produce_unit(cruiser, "player1")


class TestRule17BlockadeRestriction:
    """Test blockade capture restriction (Rule 17.6)."""

    def test_blockaded_player_cannot_capture(self) -> None:
        """Test that blockaded players cannot capture from blockading players.

        LRR Reference: Rule 17.6 - "If one or more of a player's space docks
        is being blockaded, that player cannot capture units from the
        blockading players."
        """
        from src.ti4.core.capture import CaptureManager

        # Create capture manager with blockade state
        capture_manager = CaptureManager()

        # Set up blockade: player2 is blockading player1's space dock
        capture_manager.set_blockade_state("player1", blockading_players=["player2"])

        # Create a unit owned by player2
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")

        # Player1 (blockaded) attempts to capture from player2 (blockader)
        can_capture = capture_manager.can_capture_unit(
            cruiser, capturing_player="player1", target_owner="player2"
        )

        # Should not be allowed due to blockade restriction
        assert not can_capture

    def test_non_blockaded_player_can_capture(self) -> None:
        """Test that non-blockaded players can capture normally.

        LRR Reference: Rule 17.6 - Restriction only applies to blockaded players
        """
        from src.ti4.core.capture import CaptureManager

        # Create capture manager
        capture_manager = CaptureManager()

        # Create a unit owned by player2
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")

        # Player1 (not blockaded) attempts to capture from player2
        can_capture = capture_manager.can_capture_unit(
            cruiser, capturing_player="player1", target_owner="player2"
        )

        # Should be allowed since player1 is not blockaded
        assert can_capture


class TestRule17TokenReturn:
    """Test fighter/infantry token return rules (Rule 17.4)."""

    def test_return_fighter_token_to_supply(self) -> None:
        """Test returning captured fighter tokens to supply.

        LRR Reference: Rule 17.4c - "When a captured fighter or infantry is
        returned, it is placed in the supply."
        """
        from src.ti4.core.capture import CaptureManager

        # Create and capture a fighter
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        capture_manager = CaptureManager()
        capture_manager.capture_unit(fighter, capturing_player="player2")

        # Verify token was created
        assert (
            capture_manager.get_faction_sheet_tokens("player2", UnitType.FIGHTER) == 1
        )

        # Return the fighter token
        capture_manager.return_fighter_infantry_token("player2", UnitType.FIGHTER)

        # Verify token was removed from faction sheet
        assert (
            capture_manager.get_faction_sheet_tokens("player2", UnitType.FIGHTER) == 0
        )

        # Verify token was returned to supply (implementation detail)
        assert capture_manager.get_supply_tokens(UnitType.FIGHTER) >= 1

    def test_return_infantry_token_to_supply(self) -> None:
        """Test returning captured infantry tokens to supply.

        LRR Reference: Rule 17.4c - Infantry tokens returned to supply like fighters
        """
        from src.ti4.core.capture import CaptureManager

        # Create and capture infantry
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        capture_manager = CaptureManager()
        capture_manager.capture_unit(infantry, capturing_player="player2")

        # Verify token was created
        assert (
            capture_manager.get_faction_sheet_tokens("player2", UnitType.INFANTRY) == 1
        )

        # Return the infantry token
        capture_manager.return_fighter_infantry_token("player2", UnitType.INFANTRY)

        # Verify token was removed from faction sheet
        assert (
            capture_manager.get_faction_sheet_tokens("player2", UnitType.INFANTRY) == 0
        )

        # Verify token was returned to supply
        assert capture_manager.get_supply_tokens(UnitType.INFANTRY) >= 1
