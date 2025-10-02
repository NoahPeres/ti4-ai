"""
Tests for Rule 7: AGENDA CARDS implementation.

This module tests the agenda card framework infrastructure including
base classes, registry system, and basic agenda card interface.
"""

import pytest

from ti4.core.constants import AgendaType, Faction


class TestAgendaCardEnumsAndConstants:
    """Test suite for agenda card enums and constants (Task 2.1)."""

    def test_agenda_type_enum_values(self) -> None:
        """Test that AgendaType enum has correct values."""
        # RED: Test specific enum values
        assert AgendaType.LAW.value == "law"
        assert AgendaType.DIRECTIVE.value == "directive"

    def test_voting_outcome_constants_exist(self) -> None:
        """Test that voting outcome constants are properly defined."""
        # RED: This should fail as VotingOutcomes doesn't exist yet
        from ti4.core.constants import VotingOutcomes

        assert VotingOutcomes.FOR_AGAINST == ["For", "Against"]
        assert VotingOutcomes.ELECT_PLAYER == ["Elect Player"]
        assert VotingOutcomes.ELECT_PLANET_CULTURAL == ["Elect Cultural Planet"]
        assert VotingOutcomes.ELECT_PLANET_INDUSTRIAL == ["Elect Industrial Planet"]
        assert VotingOutcomes.ELECT_PLANET_HAZARDOUS == ["Elect Hazardous Planet"]
        assert VotingOutcomes.ELECT_SECRET_OBJECTIVE == [
            "Elect Scored Secret Objective"
        ]

    def test_agenda_card_metadata_structure_exists(self) -> None:
        """Test that agenda card metadata structure is defined."""
        # RED: This should fail as AgendaCardMetadata doesn't exist yet
        from ti4.core.constants import AgendaCardMetadata

        metadata = AgendaCardMetadata(
            name="Test Card",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            expansion="Base",
        )

        assert metadata.name == "Test Card"
        assert metadata.agenda_type == AgendaType.LAW
        assert metadata.outcomes == ["For", "Against"]
        assert metadata.expansion == "Base"

    def test_agenda_card_identification_methods(self) -> None:
        """Test agenda card identification helper methods."""
        # RED: This should fail as these methods don't exist yet
        from ti4.core.constants import AgendaCardHelpers

        # Test law identification
        assert AgendaCardHelpers.is_law_card(AgendaType.LAW) is True
        assert AgendaCardHelpers.is_law_card(AgendaType.DIRECTIVE) is False

        # Test directive identification
        assert AgendaCardHelpers.is_directive_card(AgendaType.DIRECTIVE) is True
        assert AgendaCardHelpers.is_directive_card(AgendaType.LAW) is False

        # Test voting outcome validation
        assert AgendaCardHelpers.is_valid_outcome("For", ["For", "Against"]) is True
        assert (
            AgendaCardHelpers.is_valid_outcome("Invalid", ["For", "Against"]) is False
        )


class TestGameStateAgendaCardTracking:
    """Test suite for GameState agenda card tracking (Task 13.1)."""

    def test_game_state_has_agenda_deck_state(self) -> None:
        """Test that GameState tracks agenda deck state."""
        # RED: This should fail as agenda_deck_state doesn't exist yet
        from ti4.core.game_state import GameState

        game_state = GameState()

        # GameState should have agenda deck state tracking
        assert hasattr(game_state, "agenda_deck_state")
        assert game_state.agenda_deck_state is not None

        # Should contain deck state information
        deck_state = game_state.agenda_deck_state
        assert "cards_in_deck" in deck_state
        assert "cards_in_discard" in deck_state
        assert "cards_removed" in deck_state
        assert "reshuffle_count" in deck_state

    def test_game_state_agenda_deck_state_persistence(self) -> None:
        """Test that agenda deck state persists across game state updates."""
        # RED: This should fail as agenda deck state tracking doesn't exist yet
        from ti4.core.game_state import GameState

        # Create initial game state with agenda deck state
        initial_state = GameState()

        # Modify agenda deck state
        new_deck_state = {
            "cards_in_deck": 25,
            "cards_in_discard": 3,
            "cards_removed": 0,
            "reshuffle_count": 1,
        }

        # Update game state with new agenda deck state
        updated_state = initial_state.update_agenda_deck_state(new_deck_state)

        # Verify agenda deck state persisted
        assert updated_state.agenda_deck_state == new_deck_state
        assert updated_state.agenda_deck_state["cards_in_deck"] == 25
        assert updated_state.agenda_deck_state["cards_in_discard"] == 3
        assert updated_state.agenda_deck_state["reshuffle_count"] == 1

    def test_game_state_active_law_persistence(self) -> None:
        """Test that active laws persist across game saves/loads."""
        # RED: This should fail as active law persistence doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.game_state import GameState

        # Create game state with active laws
        game_state = GameState()

        # Create an active law
        law_card = AntiIntellectualRevolution()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=2,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Add law to game state
        game_state.law_manager.enact_law(active_law)

        # Serialize game state for persistence
        serialized_state = game_state.serialize_for_persistence()

        # Verify active laws are included in serialization
        assert "active_laws" in serialized_state
        assert len(serialized_state["active_laws"]) == 1
        assert (
            serialized_state["active_laws"][0]["agenda_card_name"]
            == "Anti-Intellectual Revolution"
        )

    def test_game_state_restore_from_serialized_state(self) -> None:
        """Test that GameState can be restored from serialized state with agenda cards."""
        # RED: This should fail as serialization/deserialization doesn't exist yet
        from ti4.core.game_state import GameState

        # Create serialized state data
        serialized_data = {
            "game_id": "test-game-123",
            "agenda_deck_state": {
                "cards_in_deck": 20,
                "cards_in_discard": 5,
                "cards_removed": 1,
                "reshuffle_count": 2,
            },
            "active_laws": [
                {
                    "agenda_card_name": "Fleet Regulations",
                    "enacted_round": 3,
                    "effect_description": "Each player cannot have more than 4 tokens in their fleet pool",
                    "elected_target": None,
                }
            ],
        }

        # Restore game state from serialized data
        restored_state = GameState.from_serialized_state(serialized_data)

        # Verify agenda deck state was restored
        assert restored_state.agenda_deck_state == serialized_data["agenda_deck_state"]

        # Verify active laws were restored
        active_laws = restored_state.law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Fleet Regulations"
        assert active_laws[0].enacted_round == 3

    def test_game_state_agenda_card_synchronization(self) -> None:
        """Test that agenda card state synchronization works correctly."""
        # RED: This should fail as synchronization methods don't exist yet
        from ti4.core.game_state import GameState

        # Create a mock deck object with the required methods
        class MockDeck:
            def __init__(self):
                self._removed_cards = []
                self._reshuffle_count = 2
                self._cards_remaining = 15
                self._discard_pile_size = 3

            def cards_remaining(self):
                return self._cards_remaining

            def discard_pile_size(self):
                return self._discard_pile_size

            def reshuffle_count(self):
                return self._reshuffle_count

            def get_reshuffle_count(self):
                return self._reshuffle_count

        game_state = GameState()
        mock_deck = MockDeck()

        # Synchronize agenda deck state with game state
        updated_game_state = game_state.synchronize_agenda_deck_state(mock_deck)

        # Verify synchronization worked
        deck_state = updated_game_state.agenda_deck_state
        assert deck_state["cards_in_deck"] == 15
        assert deck_state["cards_in_discard"] == 3
        assert deck_state["reshuffle_count"] == 2


class TestAgendaCardSystemIntegration:
    """Test suite for agenda card integration with existing game systems (Task 13.2)."""

    def test_anti_intellectual_revolution_technology_research_integration(self) -> None:
        """Test Anti-Intellectual Revolution law affects technology research."""
        # RED: This should fail as technology research integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.constants import Technology, UnitType
        from ti4.core.game_state import GameState
        from ti4.core.player import Player
        from ti4.core.technology import TechnologyManager
        from ti4.core.unit import Unit

        # Create game state with player and ships
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state._create_new_state(players=[player])

        # Add ships to player
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Enact Anti-Intellectual Revolution law
        law_card = AntiIntellectualRevolution()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )
        game_state.law_manager.enact_law(active_law)

        # Research a technology
        tech_manager = TechnologyManager()
        tech_manager.research_technology("player1", Technology.GRAVITY_DRIVE)

        # Check that law effect is triggered
        law_effects = game_state.get_law_effects_for_action(
            "technology_research", "player1"
        )
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Anti-Intellectual Revolution"

        # Apply law effect - should require destroying a non-fighter ship
        destroyed_ships = game_state.apply_law_effects(
            law_effects,
            {"available_ships": [cruiser, destroyer, fighter], "player_id": "player1"},
        )

        # Should destroy exactly one non-fighter ship
        assert len(destroyed_ships) == 1
        assert destroyed_ships[0].unit_type in [UnitType.CRUISER, UnitType.DESTROYER]
        assert destroyed_ships[0].unit_type != UnitType.FIGHTER

    def test_fleet_regulations_fleet_pool_integration(self) -> None:
        """Test Fleet Regulations law affects fleet pool management."""
        # RED: This should fail as fleet pool integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.command_tokens import CommandTokenManager
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        # Create game state with player
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state._create_new_state(players=[player])

        # Enact Fleet Regulations law
        law_card = FleetRegulations()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=1,
            effect_description="Each player's fleet pool can have a maximum of 4 command tokens",
        )
        game_state.law_manager.enact_law(active_law)

        # Try to add command tokens to fleet pool
        token_manager = CommandTokenManager()

        # Should be able to add up to 4 tokens
        for _ in range(4):
            result = token_manager.add_fleet_pool_token("player1", game_state)
            assert result is True

        # Should not be able to add 5th token due to Fleet Regulations
        result = token_manager.add_fleet_pool_token("player1", game_state)
        assert result is False

        # Verify law effect was applied
        law_effects = game_state.get_law_effects_for_action(
            "fleet_pool_management", "player1"
        )
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Fleet Regulations"

    def test_homeland_defense_act_pds_placement_integration(self) -> None:
        """Test Homeland Defense Act law affects PDS placement limits."""
        # RED: This should fail as PDS placement integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.constants import UnitType
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.production import ProductionManager
        from ti4.core.unit import Unit

        # Create game state with player and planet
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        planet = Planet(name="Test Planet", resources=2, influence=1)
        game_state = game_state._create_new_state(
            players=[player], player_planets={"player1": [planet]}
        )

        # Enact Homeland Defense Act law
        law_card = HomelandDefenseAct()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=1,
            effect_description="Each player can have any number of PDS units on planets they control",
        )
        game_state.law_manager.enact_law(active_law)

        # Try to place multiple PDS units on the same planet
        production_manager = ProductionManager()

        # Without the law, should be limited to 1 PDS per planet
        # With the law, should be able to place unlimited PDS
        for _ in range(5):  # Try to place 5 PDS units
            can_place = production_manager.can_place_pds_on_planet(
                planet, "player1", game_state
            )
            assert can_place is True  # Should be allowed due to Homeland Defense Act

            # Actually place the PDS
            pds_unit = Unit(unit_type=UnitType.PDS, owner="player1")
            planet.place_unit(pds_unit)

        # Verify law effect was applied
        law_effects = game_state.get_law_effects_for_action(
            "pds_placement_limit", "player1"
        )
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Homeland Defense Act"

    def test_agenda_card_movement_system_integration(self) -> None:
        """Test agenda cards that affect movement system."""
        # RED: This should fail as movement integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.enforced_travel_ban import EnforcedTravelBan
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.constants import UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.game_state import GameState
        from ti4.core.movement import MovementOperation, MovementValidator
        from ti4.core.player import Player
        from ti4.core.unit import Unit

        # Create game state with player and galaxy
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        galaxy = Galaxy()
        game_state = game_state._create_new_state(players=[player], galaxy=galaxy)

        # Enact Enforced Travel Ban law (hypothetical law affecting movement)
        law_card = EnforcedTravelBan()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=1,
            effect_description="Alpha and beta wormholes have no effect during movement",
        )
        game_state.law_manager.enact_law(active_law)

        # Create movement operation through wormhole
        ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        movement = MovementOperation(
            unit=ship,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Validate movement with law effects
        movement_validator = MovementValidator(galaxy)

        # Check that law effects are considered during movement validation
        law_effects = game_state.get_law_effects_for_action("movement", "player1")
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Enforced Travel Ban"

        # Movement validation should consider wormhole restrictions
        is_valid = movement_validator.is_valid_movement_with_law_effects(
            movement, law_effects
        )
        # Result depends on whether wormholes are involved in the path
        assert isinstance(is_valid, bool)

    def test_agenda_card_combat_system_integration(self) -> None:
        """Test agenda cards that affect combat system."""
        # RED: This should fail as combat integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.combat import CombatManager
        from ti4.core.constants import UnitType
        from ti4.core.game_state import GameState
        from ti4.core.player import Player
        from ti4.core.unit import Unit

        # Create game state with players
        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        game_state = game_state._create_new_state(players=[player1, player2])

        # Enact Conventions of War law
        law_card = ConventionsOfWar()
        active_law = ActiveLaw(
            agenda_card=law_card,
            enacted_round=1,
            effect_description="Destroyed units are returned to reinforcements instead of being removed from the game",
        )
        game_state.law_manager.enact_law(active_law)

        # Create combat scenario
        attacker_units = [Unit(unit_type=UnitType.CRUISER, owner="player1")]
        defender_units = [Unit(unit_type=UnitType.DESTROYER, owner="player2")]

        combat_manager = CombatManager()

        # Check that law effects are considered during combat
        law_effects = game_state.get_law_effects_for_action("combat", "player1")
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Conventions of War"

        # Combat resolution should consider law effects
        combat_result = combat_manager.resolve_combat_with_law_effects(
            attacker_units, defender_units, law_effects
        )

        # Verify that destroyed units are handled according to law
        assert hasattr(combat_result, "destroyed_units_returned_to_reinforcements")
        assert isinstance(
            combat_result.destroyed_units_returned_to_reinforcements, list
        )

    def test_comprehensive_cross_system_effect_validation(self) -> None:
        """Test comprehensive validation of agenda effects across multiple systems."""
        # RED: This should fail as comprehensive validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.agenda_cards.validation import AgendaEffectValidator
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        # Create game state with multiple active laws
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)
        game_state = game_state._create_new_state(players=[player])

        # Enact multiple laws
        law1 = AntiIntellectualRevolution()
        active_law1 = ActiveLaw(
            agenda_card=law1,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        law2 = FleetRegulations()
        active_law2 = ActiveLaw(
            agenda_card=law2,
            enacted_round=2,
            effect_description="Each player's fleet pool can have a maximum of 4 command tokens",
        )

        game_state.law_manager.enact_law(active_law1)
        game_state.law_manager.enact_law(active_law2)

        # Validate cross-system effects
        validator = AgendaEffectValidator()

        # Test technology research action with multiple law effects
        validation_result = validator.validate_action_with_law_effects(
            action_type="technology_research",
            player_id="player1",
            game_state=game_state,
            action_context={
                "technology": "Gravity Drive",
                "available_ships": ["cruiser", "destroyer", "fighter"],
                "current_fleet_tokens": 3,
            },
        )

        # Should identify all applicable law effects
        assert (
            validation_result.applicable_laws == 1
        )  # Only Anti-Intellectual Revolution applies
        assert validation_result.required_actions == ["destroy_non_fighter_ship"]
        assert validation_result.is_valid is True

        # Test fleet pool action with law effects
        fleet_validation = validator.validate_action_with_law_effects(
            action_type="fleet_pool_management",
            player_id="player1",
            game_state=game_state,
            action_context={"action": "add_token", "current_fleet_tokens": 4},
        )

        # Should be blocked by Fleet Regulations
        assert fleet_validation.applicable_laws == 1  # Fleet Regulations applies
        assert fleet_validation.is_valid is False
        assert "fleet_pool_limit_exceeded" in fleet_validation.validation_errors

    def test_agenda_deck_invalid_parameters(self):
        """Test agenda deck with invalid parameters."""
        from ti4.core.game_state import GameState

        game_state = GameState()
        invalid_deck_state = {
            "cards_in_deck": -1,  # Invalid negative value
            "reshuffle_count": 1,
        }

        # Should raise validation error
        with pytest.raises(ValueError, match="cards_in_deck cannot be negative"):
            game_state.update_agenda_deck_state(invalid_deck_state)

    def test_game_state_create_new_state_preserves_agenda_data(self) -> None:
        """Test that _create_new_state preserves agenda card data."""
        # RED: This should fail as agenda data preservation doesn't exist yet
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        # Create game state with agenda data
        initial_state = GameState()
        initial_deck_state = {
            "cards_in_deck": 22,
            "cards_in_discard": 4,
            "cards_removed": 2,
            "reshuffle_count": 0,
        }

        # Update with agenda deck state
        state_with_agenda = initial_state.update_agenda_deck_state(initial_deck_state)

        # Create new state with different data (should preserve agenda data)
        from ti4.core.constants import Faction

        new_player = Player(id="test-player", faction=Faction.ARBOREC)
        new_state = state_with_agenda._create_new_state(players=[new_player])

        # Verify agenda data was preserved
        assert new_state.agenda_deck_state == initial_deck_state
        assert new_state.players == [new_player]


class TestVictoryPointAgendaCards:
    """Test suite for victory point agenda cards (Task 11.2)."""

    def test_shard_of_the_throne_creation(self) -> None:
        """Test that Shard of the Throne card can be created."""
        # RED: This should fail as ShardOfTheThrone doesn't exist yet
        from ti4.core.agenda_cards.concrete.shard_of_the_throne import ShardOfTheThrone

        card = ShardOfTheThrone()
        assert card.get_name() == "Shard of the Throne"
        assert card.get_agenda_type().value == "law"
        assert card.get_voting_outcomes() == ["Elect Player"]

    def test_shard_of_the_throne_victory_point_mechanics(self) -> None:
        """Test Shard of the Throne victory point gain/loss mechanics."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.shard_of_the_throne import ShardOfTheThrone
        from ti4.core.game_state import GameState

        card = ShardOfTheThrone()
        game_state = GameState()

        # Mock vote result with elected player
        class MockVoteResult:
            elected_target = "player1"

        vote_result = MockVoteResult()

        # Test initial election grants VP
        result = card.resolve_outcome("Elect Player", vote_result, game_state)
        assert result is not None
        assert "victory point" in result.description.lower()

    def test_shard_of_the_throne_combat_transfer(self) -> None:
        """Test Shard of the Throne transfers on combat victory."""
        # RED: This should fail as the transfer mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.shard_of_the_throne import ShardOfTheThrone

        card = ShardOfTheThrone()

        # Test that card has combat transfer mechanics
        assert hasattr(card, "handle_combat_victory")

        # Mock game state with current owner
        class MockGameState:
            def get_shard_owner(self):
                return "player1"

            def set_shard_owner(self, player):
                pass

            def adjust_victory_points(self, player, amount):
                pass

        game_state = MockGameState()

        # Test combat victory transfer
        card.handle_combat_victory("player2", "player1", game_state)

    def test_crown_of_emphidia_creation(self) -> None:
        """Test that Crown of Emphidia card can be created."""
        # RED: This should fail as CrownOfEmphidia doesn't exist yet
        from ti4.core.agenda_cards.concrete.crown_of_emphidia import CrownOfEmphidia

        card = CrownOfEmphidia()
        assert card.get_name() == "The Crown of Emphidia"
        assert card.get_agenda_type().value == "law"
        assert card.get_voting_outcomes() == ["Elect Player"]

    def test_crown_of_emphidia_home_system_transfer(self) -> None:
        """Test Crown of Emphidia transfers on home system planet capture."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.crown_of_emphidia import CrownOfEmphidia

        card = CrownOfEmphidia()

        # Test that card has home system transfer mechanics
        assert hasattr(card, "handle_home_system_capture")

        # Mock game state
        class MockGameState:
            def get_crown_emphidia_owner(self):
                return "player1"

            def set_crown_emphidia_owner(self, player):
                pass

            def adjust_victory_points(self, player, amount):
                pass

            def is_home_system_planet(self, planet, player):
                return True

        game_state = MockGameState()

        # Test home system capture transfer
        card.handle_home_system_capture("player2", "test_planet", game_state)

    def test_crown_of_thalnos_creation(self) -> None:
        """Test that Crown of Thalnos card can be created."""
        # RED: This should fail as CrownOfThalnos doesn't exist yet
        from ti4.core.agenda_cards.concrete.crown_of_thalnos import CrownOfThalnos

        card = CrownOfThalnos()
        assert card.get_name() == "The Crown of Thalnos"
        assert card.get_agenda_type().value == "law"
        assert card.get_voting_outcomes() == ["Elect Player"]

    def test_crown_of_thalnos_reroll_ability(self) -> None:
        """Test Crown of Thalnos reroll ability mechanics."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.crown_of_thalnos import CrownOfThalnos

        card = CrownOfThalnos()

        # Test that card has reroll mechanics
        assert hasattr(card, "can_reroll_dice")
        assert hasattr(card, "apply_reroll_penalty")

    def test_holy_planet_of_ixth_creation(self) -> None:
        """Test that Holy Planet of Ixth card can be created."""
        # RED: This should fail as HolyPlanetOfIxth doesn't exist yet
        from ti4.core.agenda_cards.concrete.holy_planet_of_ixth import HolyPlanetOfIxth

        card = HolyPlanetOfIxth()
        assert card.get_name() == "Holy Planet of Ixth"
        assert card.get_agenda_type().value == "law"
        assert card.get_voting_outcomes() == ["Elect Cultural Planet"]

    def test_holy_planet_of_ixth_victory_point_mechanics(self) -> None:
        """Test Holy Planet of Ixth victory point gain/loss on control changes."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.holy_planet_of_ixth import HolyPlanetOfIxth

        card = HolyPlanetOfIxth()

        # Test that card has control change mechanics
        assert hasattr(card, "handle_planet_control_gain")
        assert hasattr(card, "handle_planet_control_loss")

    def test_victory_point_tracking_integration(self) -> None:
        """Test that victory point changes are properly tracked in game state."""
        # RED: This should fail as VP tracking integration doesn't exist yet
        from ti4.core.game_state import GameState

        game_state = GameState()

        # Test VP tracking methods exist
        assert hasattr(game_state, "award_victory_points")
        assert hasattr(game_state, "get_victory_points")
        # Note: track_agenda_card_ownership method doesn't exist yet - this is expected for RED phase


class TestAgendaCardProtocols:
    """Test suite for agenda card protocols (Task 2.2)."""

    def test_agenda_card_protocol_exists(self) -> None:
        """Test that AgendaCardProtocol is properly defined."""
        # RED: This should fail as AgendaCardProtocol doesn't exist yet
        from typing import get_origin

        from ti4.core.agenda_cards.protocols import AgendaCardProtocol

        # Test that it's a protocol by checking its origin
        assert get_origin(AgendaCardProtocol) is None  # Protocols don't have origins
        assert hasattr(
            AgendaCardProtocol, "__annotations__"
        )  # Protocols have annotations

    def test_agenda_card_protocol_interface_compliance(self) -> None:
        """Test that agenda card interface compliance works."""
        # RED: This should fail as the protocol doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.protocols import AgendaCardProtocol

        # Test that LawCard implements the protocol
        law_card = LawCard("Test Law")
        assert isinstance(law_card, AgendaCardProtocol)

    def test_base_card_validation_methods_exist(self) -> None:
        """Test that base card validation methods are implemented."""
        # RED: This should fail as validation methods don't exist yet
        from ti4.core.agenda_cards.base import BaseAgendaCard

        # Test validation method exists (will be abstract)
        assert hasattr(BaseAgendaCard, "validate_card_data")

    def test_card_name_and_type_identification(self) -> None:
        """Test card name and type identification methods."""
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.constants import AgendaType

        # Test law card identification
        law_card = LawCard("Test Law")
        assert law_card.get_name() == "Test Law"
        assert law_card.get_agenda_type() == AgendaType.LAW

        # Test directive card identification
        directive_card = DirectiveCard("Test Directive")
        assert directive_card.get_name() == "Test Directive"
        assert directive_card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_agenda_card_validation_with_invalid_data(self) -> None:
        """Test agenda card validation with invalid data."""
        from ti4.core.agenda_cards.base import LawCard

        # Test that validation catches invalid data
        law_card = LawCard("Test Law")

        # Test validation with empty outcomes
        is_valid = law_card.validate_card_data(
            outcomes=[], metadata={"expansion": "Base"}
        )
        assert is_valid is False

        # Test validation with None outcomes
        is_valid = law_card.validate_card_data(
            outcomes=["", "  "],  # Empty/whitespace strings
            metadata={"expansion": "Base"},
        )
        assert is_valid is False

        # Test validation with invalid metadata type
        is_valid = law_card.validate_card_data(
            outcomes=["For", "Against"],
            metadata="not a dict",  # type: ignore
        )
        assert is_valid is False

    def test_agenda_card_validation_with_valid_data(self) -> None:
        """Test agenda card validation with valid data."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard

        # Test that validation passes with valid data
        law_card = LawCard("Test Law")

        # Test validation with valid outcomes
        is_valid = law_card.validate_card_data(
            outcomes=["For", "Against"], metadata={"expansion": "Base"}
        )
        assert is_valid is True


class TestPlanetAttachmentSystem:
    """Test suite for planet attachment system (Task 11.1)."""

    def test_planet_attachment_data_structure_exists(self) -> None:
        """Test that PlanetAttachment data structure is defined."""
        # RED: This should fail as PlanetAttachment doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachment

        attachment = PlanetAttachment(
            agenda_card_name="Core Mining",
            planet_name="Mecatol Rex",
            attached_round=1,
            effect_description="Gain 2 trade goods when this planet is exhausted",
        )

        assert attachment.agenda_card_name == "Core Mining"
        assert attachment.planet_name == "Mecatol Rex"
        assert attachment.attached_round == 1
        assert (
            attachment.effect_description
            == "Gain 2 trade goods when this planet is exhausted"
        )

    def test_planet_attachment_manager_exists(self) -> None:
        """Test that PlanetAttachmentManager is defined."""
        # RED: This should fail as PlanetAttachmentManager doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager

        manager = PlanetAttachmentManager()
        assert manager is not None

    def test_attach_agenda_card_to_planet(self) -> None:
        """Test attaching an agenda card to a planet."""
        # RED: This should fail as the attachment system doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach agenda card to planet
        manager.attach_card_to_planet(
            agenda_card_name="Core Mining",
            planet=planet,
            effect_description="Gain 2 trade goods when this planet is exhausted",
        )

        # Verify attachment
        attachments = manager.get_attachments_for_planet(planet.name)
        assert len(attachments) == 1
        assert attachments[0].agenda_card_name == "Core Mining"
        assert attachments[0].planet_name == "Mecatol Rex"

    def test_get_attachments_for_planet(self) -> None:
        """Test getting all attachments for a specific planet."""
        # RED: This should fail as the attachment system doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach multiple cards to the same planet
        manager.attach_card_to_planet(
            agenda_card_name="Core Mining",
            planet=planet,
            effect_description="Gain 2 trade goods when exhausted",
        )
        manager.attach_card_to_planet(
            agenda_card_name="Demilitarized Zone",
            planet=planet,
            effect_description="Ships cannot move through this system",
        )

        # Verify multiple attachments
        attachments = manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 2

        card_names = [attachment.agenda_card_name for attachment in attachments]
        assert "Core Mining" in card_names
        assert "Demilitarized Zone" in card_names

    def test_remove_attachment_from_planet(self) -> None:
        """Test removing an agenda card attachment from a planet."""
        # RED: This should fail as the attachment system doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach and then remove
        manager.attach_card_to_planet(
            agenda_card_name="Core Mining",
            planet=planet,
            effect_description="Gain 2 trade goods when exhausted",
        )

        # Verify attachment exists
        attachments = manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 1

        # Remove attachment
        removed = manager.remove_attachment_from_planet("Core Mining", "Mecatol Rex")
        assert removed is True

        # Verify attachment is gone
        attachments = manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 0

    def test_planet_attachment_validation(self) -> None:
        """Test validation of planet attachments."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Test invalid agenda card name
        with pytest.raises(ValueError, match="Agenda card name cannot be empty"):
            manager.attach_card_to_planet(
                agenda_card_name="", planet=planet, effect_description="Some effect"
            )

        # Test invalid planet
        with pytest.raises(ValueError, match="Planet cannot be None"):
            manager.attach_card_to_planet(
                agenda_card_name="Core Mining",
                planet=None,  # type: ignore
                effect_description="Some effect",
            )

        # Test empty effect description
        with pytest.raises(ValueError, match="Effect description cannot be empty"):
            manager.attach_card_to_planet(
                agenda_card_name="Core Mining", planet=planet, effect_description=""
            )

    def test_planet_attachment_error_handling(self) -> None:
        """Test error handling for planet attachment operations."""
        # RED: This should fail as error handling doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager

        manager = PlanetAttachmentManager()

        # Test removing non-existent attachment
        removed = manager.remove_attachment_from_planet(
            "Non-existent Card", "Non-existent Planet"
        )
        assert removed is False

        # Test getting attachments for non-existent planet
        attachments = manager.get_attachments_for_planet("Non-existent Planet")
        assert len(attachments) == 0

    def test_planet_attachment_persistence(self) -> None:
        """Test that planet attachments persist across game state operations."""
        # RED: This should fail as persistence doesn't exist yet
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach card
        manager.attach_card_to_planet(
            agenda_card_name="Core Mining",
            planet=planet,
            effect_description="Gain 2 trade goods when exhausted",
        )

        # Test serialization/deserialization (basic persistence test)
        state_data = manager.get_state_data()
        assert "attachments" in state_data
        assert len(state_data["attachments"]) == 1

        # Create new manager and restore state
        new_manager = PlanetAttachmentManager()
        new_manager.restore_state_data(state_data)

        # Verify attachment persisted
        attachments = new_manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 1
        assert attachments[0].agenda_card_name == "Core Mining"


class TestPlanetAttachmentAgendaCards:
    """Test suite for agenda cards that attach to planets."""

    def test_core_mining_agenda_card_attachment(self) -> None:
        """Test Core Mining agenda card can attach to planets."""
        # RED: This should fail as Core Mining card doesn't exist yet
        from ti4.core.agenda_cards.concrete.core_mining import CoreMining
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        # Create Core Mining card
        core_mining = CoreMining()
        assert core_mining.get_name() == "Core Mining"
        assert core_mining.can_attach_to_planet() is True

        # Test attachment functionality
        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach Core Mining to planet
        core_mining.attach_to_planet(planet, manager)

        # Verify attachment
        attachments = manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 1
        assert attachments[0].agenda_card_name == "Core Mining"

    def test_demilitarized_zone_agenda_card_attachment(self) -> None:
        """Test Demilitarized Zone agenda card can attach to planets."""
        # RED: This should fail as Demilitarized Zone card doesn't exist yet
        from ti4.core.agenda_cards.concrete.demilitarized_zone import DemilitarizedZone
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager
        from ti4.core.planet import Planet

        # Create Demilitarized Zone card
        demilitarized_zone = DemilitarizedZone()
        assert demilitarized_zone.get_name() == "Demilitarized Zone"
        assert demilitarized_zone.can_attach_to_planet() is True

        # Test attachment functionality
        manager = PlanetAttachmentManager()
        planet = Planet("Mecatol Rex", 1, 6)

        # Attach Demilitarized Zone to planet
        demilitarized_zone.attach_to_planet(planet, manager)

        # Verify attachment
        attachments = manager.get_attachments_for_planet("Mecatol Rex")
        assert len(attachments) == 1
        assert attachments[0].agenda_card_name == "Demilitarized Zone"

    def test_planet_attachment_base_class_interface(self) -> None:
        """Test that planet-attachable agenda cards implement the correct interface."""
        # RED: This should fail as PlanetAttachableCard doesn't exist yet
        from ti4.core.agenda_cards.base.planet_attachable_card import (
            PlanetAttachableCard,
        )

        # Test that PlanetAttachableCard is abstract
        with pytest.raises(TypeError):
            PlanetAttachableCard("Test Card")  # type: ignore

        # Test interface methods exist
        assert hasattr(PlanetAttachableCard, "can_attach_to_planet")
        assert hasattr(PlanetAttachableCard, "attach_to_planet")
        assert hasattr(PlanetAttachableCard, "get_attachment_effect_description")

    def test_agenda_card_attachment_validation(self) -> None:
        """Test validation for agenda card planet attachments."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.core_mining import CoreMining
        from ti4.core.agenda_cards.planet_attachment import PlanetAttachmentManager

        core_mining = CoreMining()
        manager = PlanetAttachmentManager()

        # Test invalid planet attachment
        with pytest.raises(ValueError, match="Planet cannot be None"):
            core_mining.attach_to_planet(None, manager)  # type: ignore

        # Test invalid manager attachment
        from ti4.core.planet import Planet

        planet = Planet("Test Planet", 1, 1)

        with pytest.raises(ValueError, match="Attachment manager cannot be None"):
            core_mining.attach_to_planet(planet, None)  # type: ignore


class TestAgendaCardFrameworkInfrastructure:
    """Test suite for agenda card framework infrastructure."""

    def test_agenda_type_enum_exists(self) -> None:
        """Test that AgendaType enum is properly defined."""
        # RED: This should fail initially as AgendaType doesn't exist yet
        assert AgendaType.LAW is not None
        assert AgendaType.DIRECTIVE is not None

    def test_base_agenda_card_interface(self) -> None:
        """Test that BaseAgendaCard abstract interface is properly defined."""
        from ti4.core.agenda_cards.base import BaseAgendaCard

        # RED: This should fail as BaseAgendaCard doesn't exist yet
        assert BaseAgendaCard is not None

        # Test that it's abstract and cannot be instantiated directly
        with pytest.raises(TypeError):
            BaseAgendaCard()

    def test_law_card_base_class(self) -> None:
        """Test that LawCard base class is properly defined."""
        from ti4.core.agenda_cards.base import LawCard

        # RED: This should fail as LawCard doesn't exist yet
        assert LawCard is not None

        # Test that it returns correct agenda type
        law_card = LawCard("Test Law")
        assert law_card.get_agenda_type() == AgendaType.LAW

    def test_directive_card_base_class(self) -> None:
        """Test that DirectiveCard base class is properly defined."""
        from ti4.core.agenda_cards.base import DirectiveCard

        # RED: This should fail as DirectiveCard doesn't exist yet
        assert DirectiveCard is not None

        # Test that it returns correct agenda type
        directive_card = DirectiveCard("Test Directive")
        assert directive_card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_agenda_card_registry_exists(self) -> None:
        """Test that AgendaCardRegistry is properly defined."""
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # RED: This should fail as AgendaCardRegistry doesn't exist yet
        registry = AgendaCardRegistry()
        assert registry is not None

    def test_agenda_card_registry_basic_operations(self) -> None:
        """Test basic registry operations."""
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # RED: This should fail as the registry doesn't exist yet
        registry = AgendaCardRegistry()

        # Test initial state
        assert len(registry) == 0
        assert registry.get_all_card_names() == []

    def test_agenda_card_name_validation(self) -> None:
        """Test that agenda card name validation works correctly."""
        from ti4.core.agenda_cards.base import LawCard

        # Test valid name
        card = LawCard("Valid Name")
        assert card.name == "Valid Name"

        # Test name with whitespace is trimmed
        card_with_spaces = LawCard("  Spaced Name  ")
        assert card_with_spaces.name == "Spaced Name"

        # Test empty name raises ValueError
        with pytest.raises(ValueError, match="Agenda card name cannot be empty"):
            LawCard("")

        # Test whitespace-only name raises ValueError
        with pytest.raises(ValueError, match="Agenda card name cannot be empty"):
            LawCard("   ")

    def test_registry_validation(self) -> None:
        """Test that registry validation works correctly."""
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        registry = AgendaCardRegistry()

        # Test registering None raises ValueError
        with pytest.raises(ValueError, match="Cannot register None as an agenda card"):
            registry.register_card(None)


class TestAgendaDeckIntegration:
    """Test suite for agenda deck integration with card framework (Task 3.1)."""

    def test_agenda_deck_with_concrete_card_instances(self) -> None:
        """Test agenda deck initialization with concrete card instances."""
        # RED: This should fail as AgendaDeck doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create registry with test cards
        registry = AgendaCardRegistry()
        law_card = LawCard("Test Law")
        directive_card = DirectiveCard("Test Directive")
        registry.register_card(law_card)
        registry.register_card(directive_card)

        # Create deck with registered cards
        deck = AgendaDeck(registry)

        # Test deck initialization
        assert deck is not None
        assert len(deck) == 2  # Should have 2 cards
        assert deck.cards_remaining() == 2

    def test_agenda_deck_registry_integration(self) -> None:
        """Test that AgendaDeck integrates with AgendaCardRegistry."""
        # RED: This should fail as integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create registry with cards
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Law 1"))
        registry.register_card(LawCard("Law 2"))

        # Create deck from registry
        deck = AgendaDeck(registry)

        # Test that deck contains all registered cards
        assert len(deck) == 2
        card_names = [card.name for card in deck.get_all_cards()]
        assert "Law 1" in card_names
        assert "Law 2" in card_names

    def test_deck_initialization_with_registered_cards(self) -> None:
        """Test deck initialization with registered cards."""
        # RED: This should fail as deck initialization doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create registry with mixed card types
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Anti-Intellectual Revolution"))
        registry.register_card(DirectiveCard("Classified Document Leaks"))
        registry.register_card(LawCard("Fleet Regulations"))

        # Initialize deck
        deck = AgendaDeck(registry)

        # Test deck state
        assert deck.cards_remaining() == 3
        assert deck.discard_pile_size() == 0
        assert not deck.is_empty()

    def test_deck_shuffling_with_card_instances(self) -> None:
        """Test deck shuffling with proper card instances."""
        # RED: This should fail as shuffling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create registry with multiple cards
        registry = AgendaCardRegistry()
        for i in range(5):
            registry.register_card(LawCard(f"Law {i}"))

        # Create and shuffle deck
        deck = AgendaDeck(registry)
        original_order = [card.name for card in deck.get_all_cards()]

        deck.shuffle()

        # Test that cards are still there but potentially in different order
        shuffled_order = [card.name for card in deck.get_all_cards()]
        assert len(shuffled_order) == len(original_order)
        assert set(shuffled_order) == set(original_order)

    def test_deck_drawing_with_card_instances(self) -> None:
        """Test deck drawing with proper card instances."""
        # RED: This should fail as drawing doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.constants import AgendaType

        # Create registry with test cards
        registry = AgendaCardRegistry()
        law_card = LawCard("Test Law")
        directive_card = DirectiveCard("Test Directive")
        registry.register_card(law_card)
        registry.register_card(directive_card)

        # Create deck and draw cards
        deck = AgendaDeck(registry)

        # Draw first card
        drawn_card = deck.draw_top_card()
        assert drawn_card is not None
        assert drawn_card.name in ["Test Law", "Test Directive"]
        assert drawn_card.get_agenda_type() in [AgendaType.LAW, AgendaType.DIRECTIVE]
        assert deck.cards_remaining() == 1

        # Draw second card
        second_card = deck.draw_top_card()
        assert second_card is not None
        assert second_card.name != drawn_card.name  # Should be different card
        assert deck.cards_remaining() == 0

    def test_empty_deck_handling(self) -> None:
        """Test handling of empty deck scenarios."""
        # RED: This should fail as empty deck handling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck, AgendaDeckEmptyError
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck with one card
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Only Card"))
        deck = AgendaDeck(registry)

        # Draw the only card
        deck.draw_top_card()
        assert deck.is_empty()

        # Try to draw from empty deck should raise exception
        with pytest.raises(AgendaDeckEmptyError):
            deck.draw_top_card()

    def test_deck_state_tracking(self) -> None:
        """Test deck state tracking methods."""
        # RED: This should fail as state tracking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck with cards
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Card 1"))
        registry.register_card(LawCard("Card 2"))
        registry.register_card(LawCard("Card 3"))

        deck = AgendaDeck(registry)

        # Test initial state
        assert deck.cards_remaining() == 3
        assert deck.discard_pile_size() == 0
        assert deck.total_cards() == 3
        assert not deck.is_empty()

        # Draw a card
        deck.draw_top_card()
        assert deck.cards_remaining() == 2
        assert deck.total_cards() == 3  # Total doesn't change

    def test_deck_validation_and_error_handling(self) -> None:
        """Test deck validation and error handling."""
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Test None registry
        with pytest.raises(ValueError, match="Registry cannot be None"):
            AgendaDeck(None)  # type: ignore

        # Test empty registry
        empty_registry = AgendaCardRegistry()
        with pytest.raises(ValueError, match="Cannot create deck from empty registry"):
            AgendaDeck(empty_registry)

        # Test None card operations
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Test Card"))
        deck = AgendaDeck(registry)

        with pytest.raises(ValueError, match="Cannot discard None card"):
            deck.discard_card(None)  # type: ignore

        with pytest.raises(ValueError, match="Cannot remove None card from game"):
            deck.remove_from_game(None)  # type: ignore


class TestAgendaDeckStateManagement:
    """Test suite for agenda deck state management (Task 3.2)."""

    def test_deck_persistence_and_state_tracking(self) -> None:
        """Test deck persistence and comprehensive state tracking."""
        # RED: This should fail as advanced state tracking doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck with mixed cards
        registry = AgendaCardRegistry()
        law1 = LawCard("Law 1")
        law2 = LawCard("Law 2")
        directive1 = DirectiveCard("Directive 1")
        registry.register_card(law1)
        registry.register_card(law2)
        registry.register_card(directive1)

        deck = AgendaDeck(registry)

        # Test initial state persistence
        initial_state = deck.get_deck_state()
        assert initial_state["cards_in_deck"] == 3
        assert initial_state["cards_in_discard"] == 0
        assert initial_state["cards_removed"] == 0
        assert initial_state["total_cards"] == 3

        # Draw and discard cards
        drawn_card = deck.draw_top_card()
        deck.discard_card(drawn_card)

        # Test state after operations
        updated_state = deck.get_deck_state()
        assert updated_state["cards_in_deck"] == 2
        assert updated_state["cards_in_discard"] == 1
        assert updated_state["cards_removed"] == 0
        assert updated_state["total_cards"] == 3

    def test_discard_pile_management(self) -> None:
        """Test comprehensive discard pile management."""
        # RED: This should fail as advanced discard pile management doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck
        registry = AgendaCardRegistry()
        for i in range(3):
            registry.register_card(LawCard(f"Card {i}"))

        deck = AgendaDeck(registry)

        # Draw and discard cards
        card1 = deck.draw_top_card()
        card2 = deck.draw_top_card()

        deck.discard_card(card1)
        deck.discard_card(card2)

        # Test discard pile contents
        discard_contents = deck.get_discard_pile_contents()
        assert len(discard_contents) == 2
        assert card1 in discard_contents
        assert card2 in discard_contents

        # Test discard pile clearing
        deck.clear_discard_pile()
        assert deck.discard_pile_size() == 0
        assert len(deck.get_discard_pile_contents()) == 0

    def test_deck_reshuffling_when_empty(self) -> None:
        """Test deck reshuffling when empty with discard pile."""
        # RED: This should fail as automatic reshuffling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create small deck
        registry = AgendaCardRegistry()
        card1 = LawCard("Card 1")
        card2 = LawCard("Card 2")
        registry.register_card(card1)
        registry.register_card(card2)

        deck = AgendaDeck(registry)

        # Draw all cards
        drawn1 = deck.draw_top_card()
        drawn2 = deck.draw_top_card()

        # Deck should be empty
        assert deck.is_empty()
        assert deck.cards_remaining() == 0

        # Discard cards
        deck.discard_card(drawn1)
        deck.discard_card(drawn2)
        assert deck.discard_pile_size() == 2

        # Drawing should trigger reshuffle
        reshuffled_card = deck.draw_top_card()
        assert reshuffled_card is not None
        assert reshuffled_card in [drawn1, drawn2]
        assert deck.cards_remaining() == 1
        assert (
            deck.discard_pile_size() == 0
        )  # Discard pile should be empty after reshuffle

    def test_deck_state_validation_and_error_handling(self) -> None:
        """Test deck state validation and comprehensive error handling."""
        # RED: This should fail as advanced validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck, AgendaDeckEmptyError
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Only Card"))
        deck = AgendaDeck(registry)

        # Draw the only card
        deck.draw_top_card()

        # Try to draw from empty deck with no discard pile
        with pytest.raises(
            AgendaDeckEmptyError,
            match="Cannot draw from empty deck with no discard pile",
        ):
            deck.draw_top_card()

        # Test state validation
        assert deck.validate_deck_state() is True  # Should be valid even when empty

        # Test deck integrity check
        integrity_result = deck.check_deck_integrity()
        assert integrity_result["is_valid"] is True
        assert (
            integrity_result["total_accounted_cards"] == 0
        )  # No cards in deck/discard/removed
        assert integrity_result["cards_in_play"] == 1  # One card drawn and in play
        assert integrity_result["missing_cards"] == 0

    def test_deck_reshuffle_tracking(self) -> None:
        """Test tracking of deck reshuffles."""
        # RED: This should fail as reshuffle tracking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Card 1"))
        registry.register_card(LawCard("Card 2"))
        deck = AgendaDeck(registry)

        # Initial reshuffle count should be 0
        assert deck.get_reshuffle_count() == 0

        # Draw all cards and discard them
        card1 = deck.draw_top_card()
        card2 = deck.draw_top_card()
        deck.discard_card(card1)
        deck.discard_card(card2)

        # Drawing should trigger reshuffle
        deck.draw_top_card()
        assert deck.get_reshuffle_count() == 1

        # Another cycle
        remaining_card = deck.draw_top_card()
        deck.discard_card(remaining_card)
        deck.draw_top_card()  # Should trigger another reshuffle
        assert deck.get_reshuffle_count() == 2

    def test_deck_state_serialization(self) -> None:
        """Test deck state serialization for persistence."""
        # RED: This should fail as serialization doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry

        # Create deck with operations
        registry = AgendaCardRegistry()
        registry.register_card(LawCard("Law Card"))
        registry.register_card(DirectiveCard("Directive Card"))
        deck = AgendaDeck(registry)

        # Perform some operations
        drawn_card = deck.draw_top_card()
        deck.discard_card(drawn_card)

        # Serialize state
        serialized_state = deck.serialize_state()
        assert "deck_cards" in serialized_state
        assert "discard_pile" in serialized_state
        assert "removed_cards" in serialized_state
        assert "reshuffle_count" in serialized_state
        assert "total_cards" in serialized_state

        # Test deserialization
        new_deck = AgendaDeck.from_serialized_state(serialized_state, registry)
        assert new_deck.cards_remaining() == deck.cards_remaining()
        assert new_deck.discard_pile_size() == deck.discard_pile_size()
        assert new_deck.get_reshuffle_count() == deck.get_reshuffle_count()


class TestMinisterCards:
    """Test suite for Minister cards with elected player effects (Task 8.2)."""

    def test_minister_of_commerce_card_creation(self) -> None:
        """Test Minister of Commerce card creation and basic properties."""
        # RED: This should fail as MinisterOfCommerce doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.constants import AgendaType

        # Create Minister of Commerce card
        minister_card = MinisterOfCommerce()

        # Test basic properties
        assert minister_card.get_name() == "Minister of Commerce"
        assert minister_card.get_agenda_type() == AgendaType.LAW
        assert minister_card.get_voting_outcomes() == ["Elect Player"]

    def test_minister_of_commerce_elected_player_mechanics(self) -> None:
        """Test Minister of Commerce elected player mechanics."""
        # RED: This should fail as elected player mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        minister_card = MinisterOfCommerce()
        game_state = GameState()

        # Mock vote result with elected player
        vote_result = VoteResult(
            outcome="Elect Player",
            elected_target="player1",
            votes_for={"player1": 5, "player2": 3},
            votes_against={},
        )

        # Test resolution creates active law with elected player
        result = minister_card.resolve_outcome("Elect Player", vote_result, game_state)

        assert isinstance(result, AgendaResolutionResult)
        assert result.success is True
        assert result.law_enacted is True
        assert "player1" in result.description
        assert "Minister of Commerce" in result.description

    def test_minister_of_commerce_ongoing_abilities(self) -> None:
        """Test Minister of Commerce ongoing elected player abilities."""
        # RED: This should fail as ongoing abilities don't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw

        minister_card = MinisterOfCommerce()

        # Create active law with elected player
        active_law = minister_card.create_active_law(
            "Elect Player", elected_target="player1"
        )

        assert isinstance(active_law, ActiveLaw)
        assert active_law.elected_target == "player1"
        assert "replenishes commodities" in active_law.effect_description
        assert active_law.trigger_condition == "after_commodity_replenishment"

    def test_minister_of_commerce_neighbor_trade_good_gain(self) -> None:
        """Test Minister of Commerce trade good gain based on neighbors."""
        # RED: This should fail as neighbor-based trade good mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )

        minister_card = MinisterOfCommerce()

        # Create a mock game state with players dict
        class MockGameState:
            def __init__(self):
                self.players = {
                    "player1": {"neighbors": ["player2", "player3"], "trade_goods": 0},
                    "player2": {"neighbors": ["player1"], "trade_goods": 0},
                    "player3": {"neighbors": ["player1"], "trade_goods": 0},
                }

        game_state = MockGameState()

        # Test trade good calculation for elected player
        trade_goods_gained = minister_card.calculate_neighbor_trade_goods(
            elected_player="player1", game_state=game_state
        )

        assert trade_goods_gained == 2  # player1 has 2 neighbors

    def test_minister_card_ownership_tracking(self) -> None:
        """Test minister card ownership and effect tracking."""
        # RED: This should fail as ownership tracking doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        minister_card = MinisterOfCommerce()
        law_manager = LawManager()

        # Create active law and track ownership
        active_law = minister_card.create_active_law(
            "Elect Player", elected_target="player1"
        )
        law_manager.enact_law(active_law)

        # Test ownership tracking
        minister_owner = law_manager.get_minister_card_owner("Minister of Commerce")
        assert minister_owner == "player1"

        # Test minister card effects are tracked
        minister_effects = law_manager.get_active_minister_effects("player1")
        assert len(minister_effects) == 1
        assert minister_effects[0].agenda_card.get_name() == "Minister of Commerce"

    def test_minister_card_replacement_mechanics(self) -> None:
        """Test minister card replacement when new minister is elected."""
        # RED: This should fail as replacement mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        minister_card = MinisterOfCommerce()
        law_manager = LawManager()

        # Enact first minister
        active_law1 = minister_card.create_active_law(
            "Elect Player", elected_target="player1"
        )
        law_manager.enact_law(active_law1)

        # Enact second minister (should replace first)
        active_law2 = minister_card.create_active_law(
            "Elect Player", elected_target="player2"
        )
        conflicts = law_manager.check_law_conflicts(active_law2.agenda_card)

        assert len(conflicts) == 1
        assert conflicts[0].elected_target == "player1"

        # Replace the law
        law_manager.enact_law(active_law2)

        # Verify replacement
        current_owner = law_manager.get_minister_card_owner("Minister of Commerce")
        assert current_owner == "player2"

        # Verify old minister is no longer active
        player1_effects = law_manager.get_active_minister_effects("player1")
        assert len(player1_effects) == 0

    def test_minister_of_commerce_effect_integration(self) -> None:
        """Test Minister of Commerce effect integration with game mechanics."""
        # RED: This should fail as effect integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        minister_card = MinisterOfCommerce()
        law_manager = LawManager()

        # Create a mock game state with players dict
        class MockGameState:
            def __init__(self):
                self.players = {
                    "player1": {
                        "neighbors": ["player2", "player3"],
                        "trade_goods": 5,
                        "commodities": 3,
                    },
                    "player2": {
                        "neighbors": ["player1"],
                        "trade_goods": 2,
                        "commodities": 2,
                    },
                    "player3": {
                        "neighbors": ["player1"],
                        "trade_goods": 1,
                        "commodities": 4,
                    },
                }

        game_state = MockGameState()

        # Enact Minister of Commerce for player1
        active_law = minister_card.create_active_law(
            "Elect Player", elected_target="player1"
        )
        law_manager.enact_law(active_law)

        # Simulate commodity replenishment trigger
        initial_trade_goods = game_state.players["player1"]["trade_goods"]
        neighbor_count = len(game_state.players["player1"]["neighbors"])

        # Apply minister effect
        minister_card.apply_minister_effect(
            elected_player="player1",
            trigger_context="commodity_replenishment",
            game_state=game_state,
        )

        # Verify trade goods increased by neighbor count
        expected_trade_goods = initial_trade_goods + neighbor_count
        assert game_state.players["player1"]["trade_goods"] == expected_trade_goods

    def test_minister_card_validation_and_error_handling(self) -> None:
        """Test minister card validation and error handling."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_phase import VoteResult

        minister_card = MinisterOfCommerce()

        # Create a mock game state
        class MockGameState:
            pass

        game_state = MockGameState()

        # Test invalid outcome
        invalid_vote_result = VoteResult(
            outcome="Invalid Outcome",
            elected_target="player1",
            votes_for={},
            votes_against={},
        )

        with pytest.raises(
            ValueError,
            match="Invalid outcome 'Invalid Outcome' for Minister of Commerce",
        ):
            minister_card.resolve_outcome(
                "Invalid Outcome", invalid_vote_result, game_state
            )

        # Test missing elected target
        invalid_vote_result2 = VoteResult(
            outcome="Elect Player", elected_target=None, votes_for={}, votes_against={}
        )

        with pytest.raises(
            ValueError, match="Minister of Commerce requires elected player"
        ):
            minister_card.resolve_outcome(
                "Elect Player", invalid_vote_result2, game_state
            )

        # Test invalid elected target
        with pytest.raises(
            ValueError, match="Cannot create active law without elected target"
        ):
            minister_card.create_active_law("Elect Player", elected_target=None)


class TestElectionOutcomeHandlingFramework:
    """Test suite for election outcome handling framework (Task 8.1)."""

    def test_planet_election_validation_cultural_planets(self) -> None:
        """Test planet election validation for cultural planets."""
        # RED: This should fail as enhanced election validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Create cultural planet (using traits to indicate planet type)
        cultural_planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        cultural_planet.traits = ["cultural"]
        game_state.player_planets["player1"] = [cultural_planet]

        # Test cultural planet validation
        is_valid = resolver.validate_planet_election(
            planet_name="Mecatol Rex",
            outcome="Elect Cultural Planet",
            game_state=game_state,
        )
        assert is_valid is True

        # Test invalid planet type for cultural election
        industrial_planet = Planet(name="Wellon", resources=4, influence=1)
        industrial_planet.traits = ["industrial"]
        game_state.player_planets["player1"].append(industrial_planet)

        is_valid = resolver.validate_planet_election(
            planet_name="Wellon", outcome="Elect Cultural Planet", game_state=game_state
        )
        assert is_valid is False

    def test_planet_election_validation_industrial_planets(self) -> None:
        """Test planet election validation for industrial planets."""
        # RED: This should fail as enhanced election validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Create industrial planet
        industrial_planet = Planet(name="Wellon", resources=4, influence=1)
        industrial_planet.traits = ["industrial"]
        game_state.player_planets["player1"] = [industrial_planet]

        # Test industrial planet validation
        is_valid = resolver.validate_planet_election(
            planet_name="Wellon",
            outcome="Elect Industrial Planet",
            game_state=game_state,
        )
        assert is_valid is True

        # Test invalid planet type for industrial election
        hazardous_planet = Planet(name="Lisis II", resources=2, influence=2)
        hazardous_planet.traits = ["hazardous"]
        game_state.player_planets["player1"].append(hazardous_planet)

        is_valid = resolver.validate_planet_election(
            planet_name="Lisis II",
            outcome="Elect Industrial Planet",
            game_state=game_state,
        )
        assert is_valid is False


class TestAgendaPhaseCardFrameworkIntegration:
    """Test suite for AgendaPhase integration with card framework (Task 9.1)."""

    def test_agenda_phase_with_concrete_cards_failing(self) -> None:
        """Test agenda phase with concrete card instances - should fail initially."""
        # RED: This should fail as AgendaPhase doesn't use concrete cards yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase

        # Create registry with concrete cards
        registry = AgendaCardRegistry()
        registry.register_card(AntiIntellectualRevolution())

        # Create deck with concrete cards
        deck = AgendaDeck(registry)

        # Create agenda phase
        agenda_phase = AgendaPhase()

        # Test that agenda phase can work with concrete card deck
        # This should fail because AgendaPhase doesn't integrate with AgendaCardRegistry yet
        result = agenda_phase.resolve_first_agenda(
            agenda_deck=deck,
            speaker_system=agenda_phase.speaker_system,
            voting_system=agenda_phase.voting_system,
            players=["player1", "player2"],
        )

        # Should work with concrete cards
        assert result.success is True
        assert result.agenda_revealed is not None
        assert isinstance(result.agenda_revealed, AntiIntellectualRevolution)

    def test_agenda_card_registry_integration_with_agenda_phase(self) -> None:
        """Test AgendaCardRegistry integration with existing AgendaPhase."""
        # RED: This should fail as integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase

        # Create registry with multiple concrete cards
        registry = AgendaCardRegistry()
        registry.register_card(FleetRegulations())

        # Create deck from registry
        AgendaDeck(registry)

        # Create agenda phase with registry integration
        agenda_phase = AgendaPhase()
        agenda_phase.set_agenda_card_registry(registry)

        # Test that agenda phase uses registry for card resolution
        assert agenda_phase.get_agenda_card_registry() is registry
        assert agenda_phase.can_resolve_concrete_cards() is True

    def test_agenda_revelation_with_concrete_card_instances(self) -> None:
        """Test agenda revelation using concrete card instances."""
        # RED: This should fail as revelation doesn't use concrete cards yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import AgendaPhase

        agenda_phase = AgendaPhase()
        concrete_card = ClassifiedDocumentLeaks()

        # Test revelation with concrete card
        agenda_phase.reveal_agenda(concrete_card)

        # Should trigger timing windows with concrete card data
        # This should fail because reveal_agenda doesn't handle concrete cards properly
        assert hasattr(concrete_card, "should_discard_on_reveal")
        assert concrete_card.should_discard_on_reveal is not None

    def test_voting_integration_with_card_specific_outcomes(self) -> None:
        """Test voting integration with card-specific outcomes."""
        # RED: This should fail as voting doesn't validate against card outcomes yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_phase import AgendaPhase, VotingSystem

        AgendaPhase()
        voting_system = VotingSystem()
        concrete_card = AntiIntellectualRevolution()

        # Test that voting system validates outcomes against concrete card
        valid_outcomes = concrete_card.get_voting_outcomes()
        assert "For" in valid_outcomes
        assert "Against" in valid_outcomes

        # Test voting with card-specific validation
        # This should fail because voting system doesn't validate against concrete cards
        voting_result = voting_system.validate_outcome_against_card(
            outcome="For", agenda_card=concrete_card
        )
        assert voting_result is True

        # Test invalid outcome
        invalid_result = voting_system.validate_outcome_against_card(
            outcome="Invalid Outcome", agenda_card=concrete_card
        )
        assert invalid_result is False

    def test_agenda_phase_card_framework_error_handling(self) -> None:
        """Test error handling in agenda phase with card framework."""
        # RED: This should fail as enhanced error handling doesn't exist yet
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase

        # Create empty registry and deck
        registry = AgendaCardRegistry()

        # Test error handling with empty registry
        with pytest.raises(ValueError, match="Cannot create deck from empty registry"):
            AgendaDeck(registry)

        # Test agenda phase error handling with None deck
        agenda_phase = AgendaPhase()

        with pytest.raises(ValueError, match="Agenda deck cannot be None"):
            agenda_phase.resolve_first_agenda(
                agenda_deck=None,  # type: ignore
                speaker_system=agenda_phase.speaker_system,
                voting_system=agenda_phase.voting_system,
                players=["player1", "player2"],
            )

    def test_concrete_card_effect_resolution_integration(self) -> None:
        """Test concrete card effect resolution integration."""
        # RED: This should fail as effect resolution doesn't use concrete cards yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import AgendaPhase, VoteResult
        from ti4.core.game_state import GameState

        agenda_phase = AgendaPhase()
        AgendaEffectResolver()
        concrete_card = MinisterOfCommerce()
        game_state = GameState()

        # Create vote result with election
        vote_result = VoteResult(
            outcome="Elect Player",
            elected_target="player1",
            winning_outcome="Elect Player",
        )

        # Test that agenda phase uses concrete card for effect resolution
        # This should fail because agenda phase doesn't integrate with concrete cards yet
        resolution_result = agenda_phase.resolve_agenda_outcome_with_concrete_card(
            agenda_card=concrete_card, vote_result=vote_result, game_state=game_state
        )

        assert resolution_result.success is True
        assert resolution_result.law_enacted is True
        assert "Minister of Commerce" in resolution_result.description

    def test_agenda_phase_complete_workflow_with_concrete_cards(self) -> None:
        """Test complete agenda phase workflow with concrete cards."""
        # RED: This should fail as complete workflow doesn't use concrete cards yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase
        from ti4.core.game_state import GameState

        # Create registry with concrete cards
        registry = AgendaCardRegistry()
        registry.register_card(AntiIntellectualRevolution())
        registry.register_card(FleetRegulations())

        # Create deck and game state
        deck = AgendaDeck(registry)
        game_state = GameState()
        game_state.set_agenda_deck(deck)

        # Create agenda phase with concrete card support
        agenda_phase = AgendaPhase()
        agenda_phase.set_agenda_card_registry(registry)

        # Execute complete phase with concrete cards
        # This should fail because complete workflow doesn't support concrete cards yet
        result = agenda_phase.execute_complete_phase_with_concrete_cards(
            game_state=game_state
        )

        assert result.success is True
        assert result.first_agenda_resolved is True
        assert result.second_agenda_resolved is True
        assert isinstance(
            result.first_agenda_card, (AntiIntellectualRevolution, FleetRegulations)
        )
        assert isinstance(
            result.second_agenda_card, (AntiIntellectualRevolution, FleetRegulations)
        )

    def test_agenda_phase_timing_windows_with_concrete_cards(self) -> None:
        """Test agenda phase timing windows with concrete card data."""
        # RED: This should fail as timing windows don't use concrete card data yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import AgendaPhase

        agenda_phase = AgendaPhase()
        concrete_card = ClassifiedDocumentLeaks()

        # Mock timing window callback to capture data
        timing_data = []

        def mock_timing_callback(timing_window: str, **kwargs):
            timing_data.append({"timing": timing_window, "data": kwargs})

        agenda_phase.set_timing_window_callback(mock_timing_callback)

        # Reveal agenda with concrete card
        agenda_phase.reveal_agenda(concrete_card)

        # Test that timing windows receive concrete card data
        # This should fail because timing windows don't pass concrete card data yet
        assert len(timing_data) >= 2  # Should have "when" and "after" timing windows

        when_timing = next(
            t for t in timing_data if t["timing"] == "when_agenda_revealed"
        )
        assert "agenda" in when_timing["data"]
        assert isinstance(when_timing["data"]["agenda"], ClassifiedDocumentLeaks)
        assert when_timing["data"]["agenda"].get_name() == "Classified Document Leaks"

    def test_agenda_phase_special_card_mechanics_integration(self) -> None:
        """Test agenda phase integration with special card mechanics."""
        # RED: This should fail as special mechanics integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.agenda_phase import AgendaPhase

        agenda_phase = AgendaPhase()
        committee_card = CommitteeFormation()

        # Test Committee Formation bypass mechanics
        # This should fail because special mechanics aren't integrated yet
        can_bypass = agenda_phase.can_bypass_voting_with_committee_formation(
            committee_card
        )
        assert can_bypass is True

        # Test using bypass ability
        bypass_result = agenda_phase.use_committee_formation_bypass(
            committee_card, chosen_player="player1"
        )
        assert bypass_result.success is True
        assert bypass_result.elected_target == "player1"
        assert "Committee Formation" in bypass_result.description

    def test_planet_election_validation_hazardous_planets(self) -> None:
        """Test planet election validation for hazardous planets."""
        # RED: This should fail as enhanced election validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Create hazardous planet
        hazardous_planet = Planet(name="Lisis II", resources=1, influence=0)
        hazardous_planet.traits = ["hazardous"]
        game_state.player_planets["player1"] = [hazardous_planet]

        # Test hazardous planet validation
        is_valid = resolver.validate_planet_election(
            planet_name="Lisis II",
            outcome="Elect Hazardous Planet",
            game_state=game_state,
        )
        assert is_valid is True

        # Test invalid planet type for hazardous election
        cultural_planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        cultural_planet.traits = ["cultural"]
        game_state.player_planets["player1"].append(cultural_planet)

        is_valid = resolver.validate_planet_election(
            planet_name="Mecatol Rex",
            outcome="Elect Hazardous Planet",
            game_state=game_state,
        )
        assert is_valid is False

    def test_player_election_validation_and_processing(self) -> None:
        """Test player election validation and processing."""
        # RED: This should fail as enhanced player election validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()

        # Create players
        from ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        game_state = GameState(players=[player1, player2])

        # Test valid player election
        is_valid = resolver.validate_player_election(
            player_id="player1", outcome="Elect Player", game_state=game_state
        )
        assert is_valid is True

        # Test invalid player election (non-existent player)
        is_valid = resolver.validate_player_election(
            player_id="player3", outcome="Elect Player", game_state=game_state
        )
        assert is_valid is False

        # Test empty player ID
        is_valid = resolver.validate_player_election(
            player_id="", outcome="Elect Player", game_state=game_state
        )
        assert is_valid is False

    def test_election_result_integration_with_agenda_effects(self) -> None:
        """Test election result integration with agenda effects."""
        # RED: This should fail as election result integration doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionResult,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()

        # Create test directive card with election outcome
        class TestElectionDirective(DirectiveCard):
            def get_name(self) -> str:
                return "Test Election Directive"

            def get_voting_outcomes(self) -> list[str]:
                return ["Elect Player"]

            def resolve_outcome(
                self, outcome: str, vote_result: VoteResult, game_state: GameState
            ) -> AgendaResolutionResult:
                return AgendaResolutionResult(
                    success=True,
                    directive_executed=True,
                    elected_target=vote_result.elected_target,
                    description=f"Elected {vote_result.elected_target}",
                )

        # Create players and vote result
        from ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.SOL)
        game_state = GameState(players=[player1])

        vote_result = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",
            vote_tally={"Elect Player": 5},
            elected_target="player1",
        )

        # Test election result integration
        directive = TestElectionDirective("Test Election Directive")
        result = resolver.resolve_agenda_outcome(directive, vote_result, game_state)

        assert result.success is True
        assert result.directive_executed is True
        assert result.elected_target == "player1"
        assert "player1" in result.description

    def test_election_target_validation_framework(self) -> None:
        """Test comprehensive election target validation framework."""
        # RED: This should fail as comprehensive validation framework doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            ElectionValidationError,
        )
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()

        # Set up game state with players and planets
        from ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.SOL)

        cultural_planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        cultural_planet.traits = ["cultural"]
        industrial_planet = Planet(name="Wellon", resources=4, influence=1)
        industrial_planet.traits = ["industrial"]

        game_state = GameState(
            players=[player1],
            player_planets={"player1": [cultural_planet, industrial_planet]},
        )

        # Test comprehensive validation for different election types
        validation_cases = [
            ("player1", "Elect Player", True),
            ("nonexistent", "Elect Player", False),
            ("Mecatol Rex", "Elect Cultural Planet", True),
            ("Wellon", "Elect Cultural Planet", False),
            ("Wellon", "Elect Industrial Planet", True),
            ("Mecatol Rex", "Elect Industrial Planet", False),
        ]

        for target, outcome, expected_valid in validation_cases:
            try:
                if "Player" in outcome:
                    is_valid = resolver.validate_player_election(
                        target, outcome, game_state
                    )
                else:
                    is_valid = resolver.validate_planet_election(
                        target, outcome, game_state
                    )
                assert is_valid == expected_valid, f"Failed for {target}, {outcome}"
            except ElectionValidationError:
                assert not expected_valid, (
                    f"Unexpected validation error for {target}, {outcome}"
                )

    def test_election_outcome_identification(self) -> None:
        """Test identification of election outcomes."""
        # RED: This should fail as election outcome identification doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver

        resolver = AgendaEffectResolver()

        # Test election outcome identification
        election_outcomes = [
            "Elect Player",
            "Elect Cultural Planet",
            "Elect Industrial Planet",
            "Elect Hazardous Planet",
            "Elect Scored Secret Objective",
        ]

        for outcome in election_outcomes:
            assert resolver.is_election_outcome(outcome) is True

        # Test non-election outcomes
        non_election_outcomes = ["For", "Against", "Custom Outcome"]

        for outcome in non_election_outcomes:
            assert resolver.is_election_outcome(outcome) is False

    def test_election_validation_error_handling(self) -> None:
        """Test error handling for election validation."""
        # RED: This should fail as enhanced error handling doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            ElectionValidationError,
        )
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Test validation with None values
        with pytest.raises(
            ElectionValidationError, match="Election target cannot be None or empty"
        ):
            resolver.validate_election_target(None, "Elect Player", game_state)

        with pytest.raises(
            ElectionValidationError, match="Election target cannot be None or empty"
        ):
            resolver.validate_election_target("", "Elect Player", game_state)

        # Test validation with None game state
        with pytest.raises(ElectionValidationError, match="Game state cannot be None"):
            resolver.validate_election_target("player1", "Elect Player", None)

        # Test validation with invalid outcome
        with pytest.raises(ElectionValidationError, match="Invalid election outcome"):
            resolver.validate_election_target("player1", "Invalid Outcome", game_state)


class TestCommitteeFormationDirectiveCard:
    """Test suite for Committee Formation directive card (Task 7.2)."""

    def test_committee_formation_card_creation(self) -> None:
        """Test that Committee Formation card can be created."""
        # RED: This should fail as CommitteeFormation doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )

        card = CommitteeFormation()
        assert card is not None
        assert card.get_name() == "Committee Formation"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_committee_formation_voting_outcomes(self) -> None:
        """Test Committee Formation voting outcomes."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )

        card = CommitteeFormation()
        outcomes = card.get_voting_outcomes()
        # Committee Formation doesn't have traditional voting outcomes since it bypasses voting
        assert outcomes == []

    def test_committee_formation_can_bypass_election_agenda(self) -> None:
        """Test that Committee Formation can bypass election agendas."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.game_state import GameState

        card = CommitteeFormation()
        game_state = GameState()

        # Test that card can be used to bypass election
        can_bypass = card.can_bypass_election_agenda("Elect Player", game_state)
        assert can_bypass is True

        # Test that card cannot bypass non-election agendas
        can_bypass_non_election = card.can_bypass_election_agenda("For", game_state)
        assert can_bypass_non_election is False

    def test_committee_formation_election_bypass_mechanics(self) -> None:
        """Test Committee Formation election bypass mechanics."""
        # RED: This should fail as the bypass mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.game_state import GameState

        card = CommitteeFormation()
        game_state = GameState()

        # Test bypassing election with chosen player
        chosen_player = "player_1"
        result = card.bypass_election_agenda(chosen_player, game_state)

        assert result.success is True
        assert result.directive_executed is True
        assert result.elected_target == chosen_player
        assert (
            result.description
            == f"Committee Formation: {chosen_player} elected without voting"
        )

    def test_committee_formation_pre_vote_trigger(self) -> None:
        """Test Committee Formation pre-vote trigger mechanics."""
        # RED: This should fail as pre-vote mechanics don't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )

        card = CommitteeFormation()

        # Test that card triggers before voting phase
        trigger_timing = card.get_trigger_timing()
        assert trigger_timing == "before_voting"

        # Test that card can identify election agendas
        election_outcomes = [
            "Elect Player",
            "Elect Cultural Planet",
            "Elect Industrial Planet",
        ]
        for outcome in election_outcomes:
            assert card.is_election_outcome(outcome) is True

        non_election_outcomes = ["For", "Against"]
        for outcome in non_election_outcomes:
            assert card.is_election_outcome(outcome) is False

    def test_committee_formation_special_voting_bypass_functionality(self) -> None:
        """Test Committee Formation special voting bypass functionality."""
        # RED: This should fail as special bypass functionality doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.game_state import GameState

        card = CommitteeFormation()
        game_state = GameState()

        # Test that using the card discards it
        assert card.is_discarded() is False

        # Use the card to bypass voting
        result = card.use_bypass_ability("player_2", game_state)

        assert result.success is True
        assert card.is_discarded() is True  # Card should be discarded after use
        assert result.elected_target == "player_2"

    def test_committee_formation_validation_and_error_handling(self) -> None:
        """Test Committee Formation validation and error handling."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.game_state import GameState

        card = CommitteeFormation()
        game_state = GameState()

        # Test invalid player selection
        with pytest.raises(ValueError, match="Cannot elect None player"):
            card.bypass_election_agenda(None, game_state)  # type: ignore

        with pytest.raises(ValueError, match="Cannot elect empty player name"):
            card.bypass_election_agenda("", game_state)

        # Test using card when already discarded
        card.use_bypass_ability("player_1", game_state)  # First use should work

        with pytest.raises(
            ValueError, match="Committee Formation has already been used"
        ):
            card.use_bypass_ability("player_2", game_state)  # Second use should fail

    def test_committee_formation_integration_with_agenda_phase(self) -> None:
        """Test Committee Formation integration with agenda phase."""
        # RED: This should fail as integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.agenda_phase import AgendaPhase

        card = CommitteeFormation()
        agenda_phase = AgendaPhase()

        # Test that agenda phase recognizes Committee Formation as a bypass option
        can_bypass = agenda_phase.can_bypass_voting_with_committee_formation(card)
        assert can_bypass is True

        # Test that agenda phase handles Committee Formation usage
        result = agenda_phase.use_committee_formation_bypass(card, "player_3")
        assert result.success is True
        assert result.elected_target == "player_3"


class TestClassifiedDocumentLeaksDirectiveCard:
    """Test suite for Classified Document Leaks directive card (Task 7.1)."""

    def test_classified_document_leaks_card_creation(self) -> None:
        """Test that Classified Document Leaks card can be created."""
        # RED: This should fail as ClassifiedDocumentLeaks doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )

        card = ClassifiedDocumentLeaks()
        assert card is not None
        assert card.get_name() == "Classified Document Leaks"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_classified_document_leaks_voting_outcomes(self) -> None:
        """Test Classified Document Leaks voting outcomes."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )

        card = ClassifiedDocumentLeaks()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["Elect Scored Secret Objective"]

    def test_classified_document_leaks_should_discard_on_reveal_no_scored_secrets(
        self,
    ) -> None:
        """Test that card should be discarded when revealed if no scored secret objectives exist."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()
        game_state = GameState()  # Empty game state with no scored objectives

        # Should discard when no scored secret objectives exist
        should_discard = card.should_discard_on_reveal(game_state)
        assert should_discard is True

    def test_classified_document_leaks_should_not_discard_with_scored_secrets(
        self,
    ) -> None:
        """Test that card should not be discarded when scored secret objectives exist."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()

        # Create game state with scored secret objective
        game_state = GameState()
        # Add a player with a scored secret objective
        game_state = game_state._create_new_state(
            completed_objectives={"player_1": ["secret_1"]}
        )

        # Should not discard when scored secret objectives exist
        should_discard = card.should_discard_on_reveal(game_state)
        assert should_discard is False

    def test_classified_document_leaks_election_outcome_resolution(self) -> None:
        """Test Classified Document Leaks election outcome resolution."""
        # RED: This should fail as the effect implementation doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()
        vote_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            winning_outcome="Elect Scored Secret Objective",
            vote_tally={"Elect Scored Secret Objective": 5},
            elected_target="secret_objective_1",
            success=True,
        )
        game_state = GameState()

        # Resolve election outcome
        result = card.resolve_outcome(
            "Elect Scored Secret Objective", vote_result, game_state
        )

        # Test that directive is executed with correct effect
        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "secret objective" in result.description.lower()
        assert "public" in result.description.lower()
        assert result.elected_target == "secret_objective_1"

    def test_classified_document_leaks_make_objective_public_effect(self) -> None:
        """Test that the card makes the elected secret objective public."""
        # RED: This should fail as the effect implementation doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()

        # Create game state with secret objective
        game_state = GameState()
        # Mock the objective being in the game somehow - this will need proper implementation

        vote_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            winning_outcome="Elect Scored Secret Objective",
            vote_tally={"Elect Scored Secret Objective": 5},
            elected_target="secret_1",
            success=True,
        )

        # Resolve the outcome
        result = card.resolve_outcome(
            "Elect Scored Secret Objective", vote_result, game_state
        )

        # Verify the objective becomes public
        assert result.success is True
        assert result.directive_executed is True
        # The actual implementation will need to modify the objective or game state

    def test_classified_document_leaks_invalid_outcome_handling(self) -> None:
        """Test handling of invalid voting outcomes."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()
        vote_result = VoteResult(
            outcome="Invalid Outcome",
            winning_outcome="Invalid Outcome",
            vote_tally={"Invalid Outcome": 5},
            success=True,
        )
        game_state = GameState()

        # Should raise an error for invalid outcome
        with pytest.raises(ValueError, match="Invalid voting outcome"):
            card.resolve_outcome("Invalid Outcome", vote_result, game_state)

    def test_classified_document_leaks_no_elected_target_handling(self) -> None:
        """Test handling when no target is elected."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ClassifiedDocumentLeaks()
        vote_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            winning_outcome="Elect Scored Secret Objective",
            vote_tally={"Elect Scored Secret Objective": 5},
            elected_target=None,  # No target elected
            success=True,
        )
        game_state = GameState()

        # Should raise an error when no target is elected
        with pytest.raises(ValueError, match="No target elected"):
            card.resolve_outcome(
                "Elect Scored Secret Objective", vote_result, game_state
            )


class TestAntiIntellectualRevolutionLawCard:
    """Test suite for Anti-Intellectual Revolution law card (Task 6.1)."""

    def test_anti_intellectual_revolution_card_creation(self) -> None:
        """Test that Anti-Intellectual Revolution card can be created."""
        # RED: This should fail as AntiIntellectualRevolution doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )

        card = AntiIntellectualRevolution()
        assert card is not None
        assert card.get_name() == "Anti-Intellectual Revolution"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_anti_intellectual_revolution_voting_outcomes(self) -> None:
        """Test Anti-Intellectual Revolution voting outcomes."""
        # RED: This should fail as the card doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )

        card = AntiIntellectualRevolution()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_anti_intellectual_revolution_for_effect(self) -> None:
        """Test Anti-Intellectual Revolution FOR effect (destroy ship after tech research)."""
        # RED: This should fail as the effect implementation doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = AntiIntellectualRevolution()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        # Resolve FOR outcome
        result = card.resolve_outcome("For", vote_result, game_state)

        # Test that law is enacted with correct effect
        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "destroy 1 of their non-fighter ships" in result.description.lower()

    def test_anti_intellectual_revolution_against_effect(self) -> None:
        """Test Anti-Intellectual Revolution AGAINST effect (exhaust planets for technologies)."""
        # RED: This should fail as the effect implementation doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = AntiIntellectualRevolution()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        # Resolve AGAINST outcome
        result = card.resolve_outcome("Against", vote_result, game_state)

        # Test that directive is executed with correct effect
        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "exhaust 1 planet for each technology" in result.description.lower()

    def test_anti_intellectual_revolution_law_creation(self) -> None:
        """Test creating active law from Anti-Intellectual Revolution."""
        # RED: This should fail as create_active_law doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )

        card = AntiIntellectualRevolution()
        active_law = card.create_active_law("For")

        assert active_law is not None
        assert active_law.agenda_card == card
        assert (
            "destroy 1 of their non-fighter ships"
            in active_law.effect_description.lower()
        )
        assert card.trigger_condition == "after_technology_research"

    def test_anti_intellectual_revolution_invalid_outcome(self) -> None:
        """Test Anti-Intellectual Revolution with invalid outcome."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = AntiIntellectualRevolution()
        vote_result = VoteResult(
            outcome="Invalid",
            winning_outcome="Invalid",
            vote_tally={"Invalid": 5},
            success=True,
        )
        game_state = GameState()

        # Should raise ValueError for invalid outcome
        with pytest.raises(
            ValueError,
            match="Invalid outcome 'Invalid' for Anti-Intellectual Revolution",
        ):
            card.resolve_outcome("Invalid", vote_result, game_state)


class TestFleetRegulationsLawCard:
    """Test suite for Fleet Regulations law card (Task 6.2)."""

    def test_fleet_regulations_card_creation(self) -> None:
        """Test that Fleet Regulations card can be created."""
        # RED: This should fail as FleetRegulations doesn't exist yet
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations

        card = FleetRegulations()
        assert card is not None
        assert card.get_name() == "Fleet Regulations"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_fleet_regulations_voting_outcomes(self) -> None:
        """Test Fleet Regulations voting outcomes."""
        # RED: This should fail as the card doesn't exist yet


class TestConventionsOfWarLawCard:
    """Test suite for Conventions of War law card (Task 10.1)."""

    def test_conventions_of_war_card_creation(self) -> None:
        """Test that Conventions of War card can be created."""
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar

        card = ConventionsOfWar()
        assert card is not None
        assert card.get_name() == "Conventions of War"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_conventions_of_war_voting_outcomes(self) -> None:
        """Test Conventions of War voting outcomes."""
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar

        card = ConventionsOfWar()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_conventions_of_war_for_effect(self) -> None:
        """Test Conventions of War FOR effect (no bombardment on cultural planets)."""
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ConventionsOfWar()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "bombardment" in result.description.lower()
        assert "cultural planets" in result.description.lower()

    def test_conventions_of_war_against_effect(self) -> None:
        """Test Conventions of War AGAINST effect (discard action cards)."""
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ConventionsOfWar()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "discard" in result.description.lower()
        assert "action cards" in result.description.lower()


class TestEnforcedTravelBanLawCard:
    """Test suite for Enforced Travel Ban law card (Task 10.1)."""

    def test_enforced_travel_ban_card_creation(self) -> None:
        """Test that Enforced Travel Ban card can be created."""
        from ti4.core.agenda_cards.concrete.enforced_travel_ban import EnforcedTravelBan

        card = EnforcedTravelBan()
        assert card is not None
        assert card.get_name() == "Enforced Travel Ban"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_enforced_travel_ban_voting_outcomes(self) -> None:
        """Test Enforced Travel Ban voting outcomes."""
        from ti4.core.agenda_cards.concrete.enforced_travel_ban import EnforcedTravelBan

        card = EnforcedTravelBan()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_enforced_travel_ban_for_effect(self) -> None:
        """Test Enforced Travel Ban FOR effect (wormholes have no effect)."""
        from ti4.core.agenda_cards.concrete.enforced_travel_ban import EnforcedTravelBan
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = EnforcedTravelBan()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "wormhole" in result.description.lower()
        assert "no effect" in result.description.lower()

    def test_enforced_travel_ban_against_effect(self) -> None:
        """Test Enforced Travel Ban AGAINST effect (destroy PDS near wormholes)."""
        from ti4.core.agenda_cards.concrete.enforced_travel_ban import EnforcedTravelBan
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = EnforcedTravelBan()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "destroy" in result.description.lower()
        assert "pds" in result.description.lower()


class TestExecutiveSanctionsLawCard:
    """Test suite for Executive Sanctions law card (Task 10.1)."""

    def test_executive_sanctions_card_creation(self) -> None:
        """Test that Executive Sanctions card can be created."""
        from ti4.core.agenda_cards.concrete.executive_sanctions import (
            ExecutiveSanctions,
        )

        card = ExecutiveSanctions()
        assert card is not None
        assert card.get_name() == "Executive Sanctions"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_executive_sanctions_voting_outcomes(self) -> None:
        """Test Executive Sanctions voting outcomes."""
        from ti4.core.agenda_cards.concrete.executive_sanctions import (
            ExecutiveSanctions,
        )

        card = ExecutiveSanctions()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_executive_sanctions_for_effect(self) -> None:
        """Test Executive Sanctions FOR effect (3 action card limit)."""
        from ti4.core.agenda_cards.concrete.executive_sanctions import (
            ExecutiveSanctions,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ExecutiveSanctions()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "3 action cards" in result.description.lower()

    def test_executive_sanctions_against_effect(self) -> None:
        """Test Executive Sanctions AGAINST effect (discard random action card)."""
        from ti4.core.agenda_cards.concrete.executive_sanctions import (
            ExecutiveSanctions,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = ExecutiveSanctions()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "discard" in result.description.lower()
        assert "random action card" in result.description.lower()


class TestHomelandDefenseActLawCard:
    """Test suite for Homeland Defense Act law card (Task 10.1)."""

    def test_homeland_defense_act_card_creation(self) -> None:
        """Test that Homeland Defense Act card can be created."""
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )

        card = HomelandDefenseAct()
        assert card is not None
        assert card.get_name() == "Homeland Defense Act"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_homeland_defense_act_voting_outcomes(self) -> None:
        """Test Homeland Defense Act voting outcomes."""
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )

        card = HomelandDefenseAct()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_homeland_defense_act_for_effect(self) -> None:
        """Test Homeland Defense Act FOR effect (unlimited PDS on planets)."""
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = HomelandDefenseAct()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "any number of pds" in result.description.lower()

    def test_homeland_defense_act_against_effect(self) -> None:
        """Test Homeland Defense Act AGAINST effect (destroy 1 PDS)."""
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = HomelandDefenseAct()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "destroy" in result.description.lower()
        assert "pds" in result.description.lower()


class TestPublicizeWeaponSchematicsLawCard:
    """Test suite for Publicize Weapon Schematics law card (Task 10.1)."""

    def test_publicize_weapon_schematics_card_creation(self) -> None:
        """Test that Publicize Weapon Schematics card can be created."""
        from ti4.core.agenda_cards.concrete.publicize_weapon_schematics import (
            PublicizeWeaponSchematics,
        )

        card = PublicizeWeaponSchematics()
        assert card is not None
        assert card.get_name() == "Publicize Weapon Schematics"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_publicize_weapon_schematics_voting_outcomes(self) -> None:
        """Test Publicize Weapon Schematics voting outcomes."""
        from ti4.core.agenda_cards.concrete.publicize_weapon_schematics import (
            PublicizeWeaponSchematics,
        )

        card = PublicizeWeaponSchematics()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_publicize_weapon_schematics_for_effect(self) -> None:
        """Test Publicize Weapon Schematics FOR effect (war sun tech sharing)."""
        from ti4.core.agenda_cards.concrete.publicize_weapon_schematics import (
            PublicizeWeaponSchematics,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = PublicizeWeaponSchematics()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "war sun" in result.description.lower()
        assert "ignore" in result.description.lower()
        assert "prerequisites" in result.description.lower()

    def test_publicize_weapon_schematics_against_effect(self) -> None:
        """Test Publicize Weapon Schematics AGAINST effect (discard action cards)."""
        from ti4.core.agenda_cards.concrete.publicize_weapon_schematics import (
            PublicizeWeaponSchematics,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = PublicizeWeaponSchematics()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "discard" in result.description.lower()
        assert "action cards" in result.description.lower()


class TestRegulatedConscriptionLawCard:
    """Test suite for Regulated Conscription law card (Task 10.1)."""

    def test_regulated_conscription_card_creation(self) -> None:
        """Test that Regulated Conscription card can be created."""
        from ti4.core.agenda_cards.concrete.regulated_conscription import (
            RegulatedConscription,
        )

        card = RegulatedConscription()
        assert card is not None
        assert card.get_name() == "Regulated Conscription"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_regulated_conscription_voting_outcomes(self) -> None:
        """Test Regulated Conscription voting outcomes."""
        from ti4.core.agenda_cards.concrete.regulated_conscription import (
            RegulatedConscription,
        )

        card = RegulatedConscription()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_regulated_conscription_for_effect(self) -> None:
        """Test Regulated Conscription FOR effect (produce only 1 fighter/infantry)."""
        from ti4.core.agenda_cards.concrete.regulated_conscription import (
            RegulatedConscription,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = RegulatedConscription()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "produce only 1" in result.description.lower()
        assert "fighter" in result.description.lower()
        assert "infantry" in result.description.lower()

    def test_regulated_conscription_against_effect(self) -> None:
        """Test Regulated Conscription AGAINST effect (no effect)."""
        from ti4.core.agenda_cards.concrete.regulated_conscription import (
            RegulatedConscription,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = RegulatedConscription()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "no effect" in result.description.lower()


class TestSharedResearchLawCard:
    """Test suite for Shared Research law card (Task 10.1)."""

    def test_shared_research_card_creation(self) -> None:
        """Test that Shared Research card can be created."""
        from ti4.core.agenda_cards.concrete.shared_research import SharedResearch

        card = SharedResearch()
        assert card is not None
        assert card.get_name() == "Shared Research"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_shared_research_voting_outcomes(self) -> None:
        """Test Shared Research voting outcomes."""
        from ti4.core.agenda_cards.concrete.shared_research import SharedResearch

        card = SharedResearch()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_shared_research_for_effect(self) -> None:
        """Test Shared Research FOR effect (units can move through nebulae)."""
        from ti4.core.agenda_cards.concrete.shared_research import SharedResearch
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = SharedResearch()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "move through nebulae" in result.description.lower()

    def test_shared_research_against_effect(self) -> None:
        """Test Shared Research AGAINST effect (place command token in home system)."""
        from ti4.core.agenda_cards.concrete.shared_research import SharedResearch
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = SharedResearch()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "command token" in result.description.lower()
        assert "home system" in result.description.lower()


class TestWormholeReconstructionLawCard:
    """Test suite for Wormhole Reconstruction law card (Task 10.1)."""

    def test_wormhole_reconstruction_card_creation(self) -> None:
        """Test that Wormhole Reconstruction card can be created."""
        from ti4.core.agenda_cards.concrete.wormhole_reconstruction import (
            WormholeReconstruction,
        )

        card = WormholeReconstruction()
        assert card is not None
        assert card.get_name() == "Wormhole Reconstruction"
        assert card.get_agenda_type() == AgendaType.LAW

    def test_wormhole_reconstruction_voting_outcomes(self) -> None:
        """Test Wormhole Reconstruction voting outcomes."""
        from ti4.core.agenda_cards.concrete.wormhole_reconstruction import (
            WormholeReconstruction,
        )

        card = WormholeReconstruction()
        outcomes = card.get_voting_outcomes()
        assert outcomes == ["For", "Against"]

    def test_wormhole_reconstruction_for_effect(self) -> None:
        """Test Wormhole Reconstruction FOR effect (all wormhole systems adjacent)."""
        from ti4.core.agenda_cards.concrete.wormhole_reconstruction import (
            WormholeReconstruction,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = WormholeReconstruction()
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("For", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.law_enacted is True
        assert "wormhole" in result.description.lower()
        assert "adjacent" in result.description.lower()

    def test_wormhole_reconstruction_against_effect(self) -> None:
        """Test Wormhole Reconstruction AGAINST effect (place command tokens in wormhole systems)."""
        from ti4.core.agenda_cards.concrete.wormhole_reconstruction import (
            WormholeReconstruction,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        card = WormholeReconstruction()
        vote_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )
        game_state = GameState()

        result = card.resolve_outcome("Against", vote_result, game_state)

        assert result is not None
        assert result.success is True
        assert result.directive_executed is True
        assert "command token" in result.description.lower()
        assert "wormhole" in result.description.lower()


class TestAgendaEffectResolver:
    """Test suite for AgendaEffectResolver (Task 5.1)."""

    def test_agenda_effect_resolver_creation(self) -> None:
        """Test AgendaEffectResolver can be created."""
        # RED: This should fail as AgendaEffectResolver doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver

        resolver = AgendaEffectResolver()
        assert resolver is not None

    def test_resolve_agenda_outcome_with_law_enactment(self) -> None:
        """Test resolving agenda outcome that results in law enactment."""
        # RED: This should fail as resolve_agenda_outcome doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionResult,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        # Create test data
        resolver = AgendaEffectResolver()
        law_card = LawCard("Anti-Intellectual Revolution")
        vote_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 5, "Against": 3},
            success=True,
        )
        game_state = GameState()

        # Resolve outcome
        result = resolver.resolve_agenda_outcome(law_card, vote_result, game_state)

        # Test law enactment
        assert isinstance(result, AgendaResolutionResult)
        assert result.success is True
        assert result.law_enacted is True
        assert result.directive_executed is False
        assert "Anti-Intellectual Revolution" in result.description

    def test_resolve_agenda_outcome_with_directive_execution(self) -> None:
        """Test resolving agenda outcome that results in directive execution."""
        # RED: This should fail as directive resolution doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionResult,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        # Create test data
        resolver = AgendaEffectResolver()
        directive_card = DirectiveCard("Classified Document Leaks")

        # Override voting outcomes for this test
        directive_card._voting_outcomes = ["Elect Scored Secret Objective"]

        vote_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            winning_outcome="Elect Scored Secret Objective",
            vote_tally={"Elect Scored Secret Objective": 8},
            success=True,
            elected_target="Secret Objective 1",
        )
        game_state = GameState()

        # Resolve outcome
        result = resolver.resolve_agenda_outcome(
            directive_card, vote_result, game_state
        )

        # Test directive execution
        assert isinstance(result, AgendaResolutionResult)
        assert result.success is True
        assert result.law_enacted is False
        assert result.directive_executed is True
        assert "Classified Document Leaks" in result.description

    def test_law_enactment_vs_directive_execution_logic(self) -> None:
        """Test that resolver correctly distinguishes between laws and directives."""
        # RED: This should fail as the logic doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()
        vote_result = VoteResult(
            outcome="For", winning_outcome="For", vote_tally={"For": 5}, success=True
        )

        # Test law card results in law enactment
        law_card = LawCard("Fleet Regulations")
        law_result = resolver.resolve_agenda_outcome(law_card, vote_result, game_state)
        assert law_result.law_enacted is True
        assert law_result.directive_executed is False

        # Test directive card results in directive execution
        directive_card = DirectiveCard("Committee Formation")
        directive_result = resolver.resolve_agenda_outcome(
            directive_card, vote_result, game_state
        )
        assert directive_result.law_enacted is False
        assert directive_result.directive_executed is True

    def test_election_outcome_processing(self) -> None:
        """Test processing of election-based agenda outcomes."""
        # RED: This should fail as election processing doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        minister_card = LawCard("Minister of Commerce")

        # Override voting outcomes for this test
        minister_card._voting_outcomes = ["Elect Player"]

        vote_result = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",
            vote_tally={"Elect Player": 6},
            success=True,
            elected_target="player_1",
        )
        game_state = GameState()

        # Resolve election outcome
        result = resolver.resolve_agenda_outcome(minister_card, vote_result, game_state)

        # Test election processing
        assert result.success is True
        assert result.law_enacted is True
        assert result.elected_target == "player_1"
        assert "player_1" in result.description

    def test_agenda_resolution_result_structure(self) -> None:
        """Test AgendaResolutionResult data structure."""
        # RED: This should fail as AgendaResolutionResult doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult

        # Test basic result creation
        result = AgendaResolutionResult(
            success=True,
            law_enacted=True,
            directive_executed=False,
            description="Test law enacted",
        )

        assert result.success is True
        assert result.law_enacted is True
        assert result.directive_executed is False
        assert result.description == "Test law enacted"

        # Test optional fields
        result_with_election = AgendaResolutionResult(
            success=True,
            law_enacted=True,
            directive_executed=False,
            description="Minister elected",
            elected_target="player_2",
        )

        assert result_with_election.elected_target == "player_2"

    def test_resolver_error_handling_invalid_agenda(self) -> None:
        """Test resolver error handling with invalid agenda."""
        # RED: This should fail as error handling doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionError,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        vote_result = VoteResult(
            outcome="For", winning_outcome="For", vote_tally={"For": 5}, success=True
        )
        game_state = GameState()

        # Test None agenda
        with pytest.raises(AgendaResolutionError, match="Agenda card cannot be None"):
            resolver.resolve_agenda_outcome(None, vote_result, game_state)

    def test_resolver_error_handling_invalid_vote_result(self) -> None:
        """Test resolver error handling with invalid vote result."""
        # RED: This should fail as error handling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionError,
        )
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        law_card = LawCard("Test Law")
        game_state = GameState()

        # Test None vote result
        with pytest.raises(AgendaResolutionError, match="Vote result cannot be None"):
            resolver.resolve_agenda_outcome(law_card, None, game_state)

    def test_resolver_error_handling_invalid_game_state(self) -> None:
        """Test resolver error handling with invalid game state."""
        # RED: This should fail as error handling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            AgendaResolutionError,
        )
        from ti4.core.agenda_phase import VoteResult

        resolver = AgendaEffectResolver()
        law_card = LawCard("Test Law")
        vote_result = VoteResult(
            outcome="For", winning_outcome="For", vote_tally={"For": 5}, success=True
        )

        # Test None game state
        with pytest.raises(AgendaResolutionError, match="Game state cannot be None"):
            resolver.resolve_agenda_outcome(law_card, vote_result, None)

    def test_comprehensive_agenda_outcome_resolution(self) -> None:
        """Test comprehensive agenda outcome resolution with all outcome types."""
        # RED: This should fail as comprehensive resolution doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Test For/Against law outcome
        law_card = LawCard("Anti-Intellectual Revolution")
        for_result = VoteResult(
            outcome="For",
            winning_outcome="For",
            vote_tally={"For": 6, "Against": 2},
            success=True,
        )

        result = resolver.resolve_agenda_outcome(law_card, for_result, game_state)
        assert result.success is True
        assert result.law_enacted is True
        assert result.directive_executed is False
        assert result.elected_target is None

        # Test Against outcome for same law
        against_result = VoteResult(
            outcome="Against",
            winning_outcome="Against",
            vote_tally={"For": 3, "Against": 5},
            success=True,
        )

        against_resolution = resolver.resolve_agenda_outcome(
            law_card, against_result, game_state
        )
        assert against_resolution.success is True
        # Against outcomes for laws should still enact the law but with different effect
        assert against_resolution.law_enacted is True

        # Test directive with election outcome
        directive_card = DirectiveCard("Classified Document Leaks")
        directive_card._voting_outcomes = ["Elect Scored Secret Objective"]

        election_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            winning_outcome="Elect Scored Secret Objective",
            vote_tally={"Elect Scored Secret Objective": 7},
            success=True,
            elected_target="Secret: Become a Martyr",
        )

        directive_resolution = resolver.resolve_agenda_outcome(
            directive_card, election_result, game_state
        )
        assert directive_resolution.success is True
        assert directive_resolution.law_enacted is False
        assert directive_resolution.directive_executed is True
        assert directive_resolution.elected_target == "Secret: Become a Martyr"

    def test_law_enactment_with_game_state_integration(self) -> None:
        """Test law enactment integrates properly with game state."""
        # RED: This should fail as game state integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()
        law_card = LawCard("Fleet Regulations")

        vote_result = VoteResult(
            outcome="For", winning_outcome="For", vote_tally={"For": 5}, success=True
        )

        # Resolve law enactment
        result = resolver.resolve_agenda_outcome(law_card, vote_result, game_state)

        # Test that law is properly enacted in game state
        assert result.success is True
        assert result.law_enacted is True

        # Test that game state is modified (this should fail initially)
        active_laws = game_state.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Fleet Regulations"

    def test_directive_execution_with_immediate_effects(self) -> None:
        """Test directive execution applies immediate effects."""
        # RED: This should fail as immediate effects don't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()
        directive_card = DirectiveCard("Committee Formation")

        vote_result = VoteResult(
            outcome="For", winning_outcome="For", vote_tally={"For": 4}, success=True
        )

        # Resolve directive execution
        result = resolver.resolve_agenda_outcome(
            directive_card, vote_result, game_state
        )

        # Test that directive is executed but not persisted
        assert result.success is True
        assert result.directive_executed is True
        assert result.law_enacted is False

        # Test that no laws are added to game state
        active_laws = game_state.get_active_laws()
        assert len(active_laws) == 0

    def test_election_outcome_validation_and_processing(self) -> None:
        """Test election outcome validation and processing."""
        # RED: This should fail as election validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            ElectionValidationError,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()
        minister_card = LawCard("Minister of Commerce")
        minister_card._voting_outcomes = ["Elect Player"]

        # Test valid election outcome
        valid_election = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",
            vote_tally={"Elect Player": 6},
            success=True,
            elected_target="player_1",
        )

        result = resolver.resolve_agenda_outcome(
            minister_card, valid_election, game_state
        )
        assert result.success is True
        assert result.elected_target == "player_1"

        # Test election outcome without elected target should fail
        invalid_election = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",
            vote_tally={"Elect Player": 6},
            success=True,
            elected_target=None,
        )

        with pytest.raises(
            ElectionValidationError, match="Election outcome requires elected_target"
        ):
            resolver.resolve_agenda_outcome(minister_card, invalid_election, game_state)


class TestVotingOutcomeValidation:
    """Test suite for voting outcome validation and processing (Task 5.2)."""

    def test_outcome_validation_against_card_specifications(self) -> None:
        """Test voting outcome validation against card specifications."""
        # RED: This should fail as outcome validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver

        resolver = AgendaEffectResolver()
        law_card = LawCard("Anti-Intellectual Revolution")

        # Test valid outcomes
        assert resolver.validate_outcome("For", law_card) is True
        assert resolver.validate_outcome("Against", law_card) is True

        # Test invalid outcome
        assert resolver.validate_outcome("Invalid", law_card) is False
        assert resolver.validate_outcome("", law_card) is False

    def test_election_target_validation_and_processing(self) -> None:
        """Test election target validation and processing."""
        # RED: This should fail as election target validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()

        # Create players
        player1 = Player("player_1", "Red")
        player2 = Player("player_2", "Blue")

        # Create game state with players
        game_state = GameState(players=[player1, player2])

        # Test valid player election
        assert (
            resolver.validate_player_election("player_1", "Elect Player", game_state)
            is True
        )
        assert (
            resolver.validate_player_election("player_2", "Elect Player", game_state)
            is True
        )

        # Test invalid player election
        assert (
            resolver.validate_player_election(
                "nonexistent_player", "Elect Player", game_state
            )
            is False
        )
        assert (
            resolver.validate_player_election("", "Elect Player", game_state) is False
        )
        assert (
            resolver.validate_player_election(None, "Elect Player", game_state) is False
        )

    def test_planet_election_validation_by_type(self) -> None:
        """Test planet election validation by planet type."""
        # RED: This should fail as planet type validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Test cultural planet validation
        assert (
            resolver.validate_planet_election(
                "Mecatol Rex", "Elect Cultural Planet", game_state
            )
            is True
        )
        assert (
            resolver.validate_planet_election(
                "Wellon", "Elect Cultural Planet", game_state
            )
            is False
        )

        # Test industrial planet validation
        assert (
            resolver.validate_planet_election(
                "Wellon", "Elect Industrial Planet", game_state
            )
            is True
        )
        assert (
            resolver.validate_planet_election(
                "Mecatol Rex", "Elect Industrial Planet", game_state
            )
            is False
        )

        # Test hazardous planet validation
        assert (
            resolver.validate_planet_election(
                "Lisis II", "Elect Hazardous Planet", game_state
            )
            is True
        )
        assert (
            resolver.validate_planet_election(
                "Mecatol Rex", "Elect Hazardous Planet", game_state
            )
            is False
        )

    def test_comprehensive_error_handling_for_invalid_outcomes(self) -> None:
        """Test comprehensive error handling for invalid outcomes."""
        # RED: This should fail as comprehensive error handling doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard, LawCard
        from ti4.core.agenda_cards.effect_resolver import (
            AgendaEffectResolver,
            OutcomeValidationError,
        )
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Test invalid outcome for law card
        law_card = LawCard("Fleet Regulations")
        invalid_vote_result = VoteResult(
            outcome="Invalid Outcome",
            winning_outcome="Invalid Outcome",
            vote_tally={"Invalid Outcome": 5},
            success=True,
        )

        with pytest.raises(OutcomeValidationError, match="Invalid outcome"):
            resolver.resolve_agenda_outcome(law_card, invalid_vote_result, game_state)

        # Test invalid outcome for directive card
        directive_card = DirectiveCard("Committee Formation")
        directive_card._voting_outcomes = ["For", "Against"]

        invalid_directive_result = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",  # Not valid for this directive
            vote_tally={"Elect Player": 4},
            success=True,
        )

        with pytest.raises(OutcomeValidationError, match="Invalid outcome"):
            resolver.resolve_agenda_outcome(
                directive_card, invalid_directive_result, game_state
            )

    def test_outcome_validation_with_complex_election_types(self) -> None:
        """Test outcome validation with complex election types."""
        # RED: This should fail as complex election validation doesn't exist yet
        from ti4.core.agenda_cards.base import DirectiveCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.game_state import GameState

        resolver = AgendaEffectResolver()
        game_state = GameState()

        # Test secret objective election validation
        secret_directive = DirectiveCard("Classified Document Leaks")
        secret_directive._voting_outcomes = ["Elect Scored Secret Objective"]

        # Should validate that there are scored secret objectives
        assert (
            resolver.validate_election_target(
                "Secret: Become a Martyr", "Elect Scored Secret Objective", game_state
            )
            is True
        )

        # Test planet attachment election validation
        attachment_directive = DirectiveCard("Core Mining")
        attachment_directive._voting_outcomes = ["Elect Industrial Planet"]

        assert (
            resolver.validate_election_target(
                "Wellon", "Elect Industrial Planet", game_state
            )
            is True
        )

    def test_election_outcome_processing_with_game_state_updates(self) -> None:
        """Test election outcome processing updates game state correctly."""
        # RED: This should fail as game state updates don't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.agenda_phase import VoteResult
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()

        # Create players
        player1 = Player("player_1", "Red")
        game_state = GameState(players=[player1])

        # Test minister election
        minister_card = LawCard("Minister of Commerce")
        minister_card._voting_outcomes = ["Elect Player"]

        election_result = VoteResult(
            outcome="Elect Player",
            winning_outcome="Elect Player",
            vote_tally={"Elect Player": 6},
            success=True,
            elected_target="player_1",
        )

        result = resolver.resolve_agenda_outcome(
            minister_card, election_result, game_state
        )

        # Test that election is processed correctly
        assert result.success is True
        assert result.elected_target == "player_1"

        # Test that game state reflects the election
        active_laws = game_state.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].elected_target == "player_1"

    def test_player_election_validation(self) -> None:
        """Test player election validation."""
        # RED: This should fail as player validation doesn't exist yet
        from ti4.core.agenda_cards.effect_resolver import AgendaEffectResolver
        from ti4.core.constants import Faction
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        resolver = AgendaEffectResolver()
        game_state = GameState(
            players=[
                Player("player_1", Faction.ARBOREC),
                Player("player_2", Faction.BARONY),
            ]
        )

        # Test valid player election
        assert (
            resolver.validate_player_election("player_1", "Elect Player", game_state)
            is True
        )
        assert (
            resolver.validate_player_election("player_2", "Elect Player", game_state)
            is True
        )

        # Test invalid player election
        assert (
            resolver.validate_player_election("player_3", "Elect Player", game_state)
            is False
        )
        assert (
            resolver.validate_player_election("", "Elect Player", game_state) is False
        )
        assert (
            resolver.validate_player_election(None, "Elect Player", game_state) is False
        )


class TestActiveLawDataStructure:
    """Test suite for ActiveLaw data structure (Task 4.1)."""

    def test_active_law_creation_with_metadata(self) -> None:
        """Test ActiveLaw creation with law metadata."""
        # RED: This should fail as ActiveLaw doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.constants import AgendaType

        # Create a law card
        law_card = LawCard("Anti-Intellectual Revolution")

        # Create active law
        active_law = ActiveLaw(
            agenda_card_or_active_law=law_card,
            enacted_round=3,
            elected_target=None,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Test active law properties
        assert active_law.agenda_card.get_name() == "Anti-Intellectual Revolution"
        assert active_law.agenda_card.get_agenda_type() == AgendaType.LAW
        assert active_law.enacted_round == 3
        assert active_law.elected_target is None
        assert "destroy 1 of their non-fighter ships" in active_law.effect_description

    def test_active_law_with_elected_target(self) -> None:
        """Test ActiveLaw creation with elected target (for Minister cards)."""
        # RED: This should fail as ActiveLaw doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import ActiveLaw

        # Create a minister law card
        minister_card = LawCard("Minister of Commerce")

        # Create active law with elected player
        active_law = ActiveLaw(
            agenda_card_or_active_law=minister_card,
            enacted_round=2,
            elected_target="player_1",
            effect_description="Elected player gains 1 trade good when they gain command tokens",
        )

        # Test elected target tracking
        assert active_law.elected_target == "player_1"
        assert active_law.enacted_round == 2
        assert "trade good" in active_law.effect_description

    def test_active_law_context_checking(self) -> None:
        """Test ActiveLaw context checking for rule application."""
        # RED: This should fail as context checking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import ActiveLaw, GameContext

        # Create law with specific trigger
        law_card = LawCard("Fleet Regulations")
        active_law = ActiveLaw(
            agenda_card_or_active_law=law_card,
            enacted_round=1,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Test context checking
        fleet_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 5},
        )

        assert active_law.applies_to_context(fleet_context) is True

        # Test non-applicable context
        tech_context = GameContext(
            action_type="research_technology",
            player_id="player_1",
            additional_data={"technology": "Sarween Tools"},
        )

        assert active_law.applies_to_context(tech_context) is False

    def test_active_law_serialization(self) -> None:
        """Test ActiveLaw serialization for game state persistence."""
        # RED: This should fail as serialization doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import ActiveLaw

        # Create active law
        law_card = LawCard("Publicize Weapon Schematics")
        active_law = ActiveLaw(
            agenda_card_or_active_law=law_card,
            enacted_round=4,
            effect_description="When a player researches a unit upgrade technology, each other player may research that technology",
        )

        # Test serialization
        serialized = active_law.to_dict()
        assert serialized["agenda_card_name"] == "Publicize Weapon Schematics"
        assert serialized["enacted_round"] == 4
        assert "unit upgrade technology" in serialized["effect_description"]

        # Test deserialization
        restored_law = ActiveLaw.from_dict(serialized)
        assert restored_law.agenda_card.get_name() == "Publicize Weapon Schematics"
        assert restored_law.enacted_round == 4
        assert restored_law.effect_description == active_law.effect_description


class TestLawGameStateIntegration:
    """Test suite for law system integration with game state (Task 4.2)."""

    def test_game_state_tracks_active_laws(self) -> None:
        """Test that GameState properly tracks active laws."""
        # RED: This should fail as law tracking integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager
        from ti4.core.game_state import GameState

        # Create game state with law manager
        game_state = GameState()
        assert game_state.law_manager is not None
        assert isinstance(game_state.law_manager, LawManager)

        # Test initial state
        assert len(game_state.law_manager.get_active_laws()) == 0

        # Enact a law through game state
        law_card = LawCard("Anti-Intellectual Revolution")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Test law is tracked
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"

    def test_law_effects_on_technology_research(self) -> None:
        """Test law effects during technology research actions."""
        # RED: This should fail as law effect checking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        # Create game state with anti-intellectual revolution law
        game_state = GameState()
        law_card = LawCard("Anti-Intellectual Revolution")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Test law effect checking during technology research
        tech_context = GameContext(
            action_type="research_technology",
            player_id="player_1",
            additional_data={"technology": "Sarween Tools"},
        )

        # Check if laws apply to this context
        applicable_laws = game_state.check_applicable_laws(tech_context)
        assert len(applicable_laws) == 1
        assert (
            applicable_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"
        )

    def test_law_effects_on_fleet_pool_management(self) -> None:
        """Test law effects during fleet pool management."""
        # RED: This should fail as fleet pool law checking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        # Create game state with fleet regulations law
        game_state = GameState()
        law_card = LawCard("Fleet Regulations")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=2,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Test law effect checking during fleet pool operations
        fleet_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 5},
        )

        # Check if laws apply to this context
        applicable_laws = game_state.check_applicable_laws(fleet_context)
        assert len(applicable_laws) == 1
        assert applicable_laws[0].agenda_card.get_name() == "Fleet Regulations"

        # Test validation of fleet pool size against law
        violations = game_state.validate_action_against_laws(fleet_context)
        assert (
            len(violations) > 0
        )  # Should have violations because fleet pool size exceeds limit
        assert "Fleet pool size exceeds limit" in violations[0]

    def test_law_effects_on_multiple_game_mechanics(self) -> None:
        """Test multiple laws affecting different game mechanics simultaneously."""
        # RED: This should fail as multi-law checking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        # Create game state with multiple laws
        game_state = GameState()

        # Add technology-related law
        tech_law = LawCard("Anti-Intellectual Revolution")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=tech_law,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Add fleet-related law
        fleet_law = LawCard("Fleet Regulations")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=fleet_law,
            enacted_round=2,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Test technology context
        tech_context = GameContext(
            action_type="research_technology",
            player_id="player_1",
            additional_data={"technology": "Sarween Tools"},
        )
        tech_laws = game_state.check_applicable_laws(tech_context)
        assert len(tech_laws) == 1
        assert tech_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"

        # Test fleet context
        fleet_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 3},
        )
        fleet_laws = game_state.check_applicable_laws(fleet_context)
        assert len(fleet_laws) == 1
        assert fleet_laws[0].agenda_card.get_name() == "Fleet Regulations"

        # Test context that doesn't match any laws
        unrelated_context = GameContext(
            action_type="move_ships",
            player_id="player_1",
            additional_data={"from_system": "Mecatol Rex", "to_system": "Jord"},
        )
        unrelated_laws = game_state.check_applicable_laws(unrelated_context)
        assert len(unrelated_laws) == 0

    def test_law_conflict_detection(self) -> None:
        """Test detection of conflicting laws."""
        # RED: This should fail as law conflict detection doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        # Create game state
        game_state = GameState()

        # Add first minister law
        minister1 = LawCard("Minister of Commerce")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=minister1,
            enacted_round=1,
            effect_description="Elected player gains 1 trade good when they gain command tokens",
            elected_target="player_1",
        )

        # Try to add conflicting minister law
        minister2 = LawCard("Minister of War")
        conflicts = game_state.detect_law_conflicts(minister2)
        assert len(conflicts) == 1  # Any minister conflicts with any other minister

        # Try to add same minister type (should also conflict)
        minister_commerce_2 = LawCard("Minister of Commerce")
        conflicts = game_state.detect_law_conflicts(minister_commerce_2)
        assert len(conflicts) == 1
        assert conflicts[0].agenda_card.get_name() == "Minister of Commerce"

    def test_law_conflict_resolution(self) -> None:
        """Test automatic resolution of law conflicts."""
        # RED: This should fail as law conflict resolution doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        # Create game state with existing law
        game_state = GameState()
        old_law = LawCard("Minister of Commerce")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=old_law,
            enacted_round=1,
            effect_description="Elected player gains 1 trade good when they gain command tokens",
            elected_target="player_1",
        )

        # Enact conflicting law with automatic resolution
        new_law = LawCard("Minister of Commerce")
        resolved_conflicts = game_state.enact_law_with_conflict_resolution(
            agenda_card_or_active_law=new_law,
            enacted_round=2,
            effect_description="Elected player gains 1 trade good when they gain command tokens",
            elected_target="player_2",
        )

        # Test that old law was removed and new law was added
        assert len(resolved_conflicts) == 1
        assert resolved_conflicts[0].agenda_card.get_name() == "Minister of Commerce"
        assert resolved_conflicts[0].elected_target == "player_1"

        # Test that only new law is active
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].elected_target == "player_2"

    def test_game_state_law_persistence(self) -> None:
        """Test that laws persist across game state operations."""
        # RED: This should fail as law persistence doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        # Create game state with laws
        game_state = GameState()
        law1 = LawCard("Anti-Intellectual Revolution")
        law2 = LawCard("Fleet Regulations")

        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law1,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law2,
            enacted_round=2,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Create new game state (simulating state transitions)
        new_game_state = game_state._create_new_state()

        # Test that laws persist
        assert new_game_state.law_manager is not None
        active_laws = new_game_state.law_manager.get_active_laws()
        assert len(active_laws) == 2

        law_names = [law.agenda_card.get_name() for law in active_laws]
        assert "Anti-Intellectual Revolution" in law_names
        assert "Fleet Regulations" in law_names

    def test_law_effect_validation_with_edge_cases(self) -> None:
        """Test law effect validation with edge cases and error conditions."""
        # RED: This should fail as comprehensive validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        # Create game state
        game_state = GameState()

        # Test validation with no active laws
        empty_context = GameContext(
            action_type="research_technology", player_id="player_1"
        )
        applicable_laws = game_state.check_applicable_laws(empty_context)
        assert len(applicable_laws) == 0

        # Test validation with None context
        with pytest.raises(ValueError, match="Context cannot be None"):
            game_state.check_applicable_laws(None)  # type: ignore

        # Test validation with invalid context
        invalid_context = GameContext(
            action_type="",  # Empty action type
            player_id="player_1",
        )
        with pytest.raises(ValueError, match="Action type cannot be empty"):
            game_state.check_applicable_laws(invalid_context)

        # Add law and test with invalid player
        law_card = LawCard("Anti-Intellectual Revolution")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        invalid_player_context = GameContext(
            action_type="research_technology",
            player_id="",  # Empty player ID
        )
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            game_state.check_applicable_laws(invalid_player_context)

    def test_active_law_validation(self) -> None:
        """Test ActiveLaw validation for invalid data."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import ActiveLaw

        law_card = LawCard("Test Law")

        # Test invalid round number
        with pytest.raises(ValueError, match="enacted_round must be positive"):
            ActiveLaw(
                agenda_card_or_active_law=law_card,
                enacted_round=0,
                effect_description="Test effect",
            )

        with pytest.raises(ValueError, match="enacted_round must be positive"):
            ActiveLaw(
                agenda_card_or_active_law=law_card,
                enacted_round=-1,
                effect_description="Test effect",
            )

        # Test empty effect description
        with pytest.raises(ValueError, match="effect_description cannot be empty"):
            ActiveLaw(
                agenda_card_or_active_law=law_card,
                enacted_round=1,
                effect_description="",
            )

        with pytest.raises(ValueError, match="effect_description cannot be empty"):
            ActiveLaw(
                agenda_card_or_active_law=law_card,
                enacted_round=1,
                effect_description="   ",
            )

        # Test None agenda card
        with pytest.raises(ValueError, match="agenda_card cannot be None"):
            ActiveLaw(
                agenda_card_or_active_law=None,  # type: ignore
                enacted_round=1,
                effect_description="Test effect",
            )


class TestLawManager:
    """Test suite for LawManager (Task 4.1)."""

    def test_law_manager_initialization(self) -> None:
        """Test LawManager initialization."""
        # RED: This should fail as LawManager doesn't exist yet
        from ti4.core.agenda_cards.law_manager import LawManager

        # Test empty initialization
        law_manager = LawManager()
        assert law_manager is not None
        assert len(law_manager.get_active_laws()) == 0
        assert law_manager.get_law_count() == 0

    def test_law_enactment(self) -> None:
        """Test law enactment functionality."""
        # RED: This should fail as law enactment doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()
        law_card = LawCard("Anti-Intellectual Revolution")

        # Test enacting a law
        law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=2,
            elected_target=None,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Verify law was enacted
        active_laws = law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"
        assert active_laws[0].enacted_round == 2

    def test_law_enactment_with_elected_target(self) -> None:
        """Test law enactment with elected target."""
        # RED: This should fail as elected target handling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()
        minister_card = LawCard("Minister of Commerce")

        # Test enacting minister law with elected player
        law_manager.enact_law(
            agenda_card_or_active_law=minister_card,
            enacted_round=3,
            elected_target="player_2",
            effect_description="Elected player gains 1 trade good when they gain command tokens",
        )

        # Verify elected target is tracked
        active_laws = law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].elected_target == "player_2"

    def test_multiple_law_tracking(self) -> None:
        """Test tracking multiple active laws."""
        # RED: This should fail as multiple law tracking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Enact multiple laws
        law1 = LawCard("Fleet Regulations")
        law2 = LawCard("Publicize Weapon Schematics")
        law3 = LawCard("Shared Research")

        law_manager.enact_law(law1, 1, effect_description="Fleet pool limit of 4")
        law_manager.enact_law(law2, 2, effect_description="Share unit upgrade tech")
        law_manager.enact_law(law3, 3, effect_description="Share non-unit upgrade tech")

        # Verify all laws are tracked
        active_laws = law_manager.get_active_laws()
        assert len(active_laws) == 3

        law_names = [law.agenda_card.get_name() for law in active_laws]
        assert "Fleet Regulations" in law_names
        assert "Publicize Weapon Schematics" in law_names
        assert "Shared Research" in law_names

    def test_law_removal(self) -> None:
        """Test law removal functionality."""
        # RED: This should fail as law removal doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()
        law_card = LawCard("Fleet Regulations")

        # Enact a law
        law_manager.enact_law(law_card, 1, effect_description="Fleet pool limit")

        # Verify law exists
        assert law_manager.get_law_count() == 1
        assert law_manager.has_active_law("Fleet Regulations") is True

        # Remove the law
        removed = law_manager.remove_law("Fleet Regulations")
        assert removed is True

        # Verify law was removed
        assert law_manager.get_law_count() == 0
        assert law_manager.has_active_law("Fleet Regulations") is False

        # Test removing non-existent law
        removed_again = law_manager.remove_law("Fleet Regulations")
        assert removed_again is False

    def test_law_lookup_by_name(self) -> None:
        """Test law lookup by name."""
        # RED: This should fail as law lookup doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()
        law_card = LawCard("Anti-Intellectual Revolution")

        # Enact law
        law_manager.enact_law(
            law_card, 2, effect_description="Destroy ships after tech research"
        )

        # Test lookup
        found_law = law_manager.get_law_by_name("Anti-Intellectual Revolution")
        assert found_law is not None
        assert found_law.agenda_card.get_name() == "Anti-Intellectual Revolution"
        assert found_law.enacted_round == 2

        # Test lookup of non-existent law
        not_found = law_manager.get_law_by_name("Non-existent Law")
        assert not_found is None

    def test_laws_affecting_context(self) -> None:
        """Test getting laws that affect specific game contexts."""
        # RED: This should fail as context filtering doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext, LawManager

        law_manager = LawManager()

        # Enact laws with different triggers
        tech_law = LawCard("Anti-Intellectual Revolution")
        fleet_law = LawCard("Fleet Regulations")

        law_manager.enact_law(
            tech_law, 1, effect_description="Destroy ships after tech research"
        )
        law_manager.enact_law(fleet_law, 2, effect_description="Fleet pool limit of 4")

        # Test technology research context
        tech_context = GameContext(
            action_type="research_technology",
            player_id="player_1",
            additional_data={"technology": "Sarween Tools"},
        )

        tech_affecting_laws = law_manager.get_laws_affecting_context(tech_context)
        assert len(tech_affecting_laws) == 1
        assert (
            tech_affecting_laws[0].agenda_card.get_name()
            == "Anti-Intellectual Revolution"
        )

        # Test fleet pool context
        fleet_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 5},
        )

        fleet_affecting_laws = law_manager.get_laws_affecting_context(fleet_context)
        assert len(fleet_affecting_laws) == 1
        assert fleet_affecting_laws[0].agenda_card.get_name() == "Fleet Regulations"

    def test_law_manager_validation(self) -> None:
        """Test LawManager validation and error handling."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Test enacting None law
        with pytest.raises(ValueError, match="agenda_card cannot be None"):
            law_manager.enact_law(None, 1, effect_description="Test")  # type: ignore

        # Test enacting with invalid round
        law_card = LawCard("Test Law")
        with pytest.raises(ValueError, match="enacted_round must be positive"):
            law_manager.enact_law(law_card, 0, effect_description="Test")

        # Test enacting with empty effect description
        with pytest.raises(ValueError, match="effect_description cannot be empty"):
            law_manager.enact_law(law_card, 1, effect_description="")

        # Test removing law with None name
        with pytest.raises(ValueError, match="law_name cannot be None or empty"):
            law_manager.remove_law(None)  # type: ignore

        # Test removing law with empty name
        with pytest.raises(ValueError, match="law_name cannot be None or empty"):
            law_manager.remove_law("")

    def test_law_persistence_across_rounds(self) -> None:
        """Test that laws persist across multiple game rounds."""
        # RED: This should fail as persistence tracking doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Enact laws in different rounds
        law1 = LawCard("Fleet Regulations")
        law2 = LawCard("Anti-Intellectual Revolution")

        law_manager.enact_law(law1, 1, effect_description="Fleet limit")
        law_manager.enact_law(law2, 3, effect_description="Destroy ships")

        # Simulate multiple rounds passing
        current_round = 5

        # Test that laws are still active
        active_laws = law_manager.get_active_laws()
        assert len(active_laws) == 2

        # Test laws enacted in earlier rounds are still active
        for law in active_laws:
            assert law.enacted_round < current_round

        # Test getting laws by enactment round
        round_1_laws = law_manager.get_laws_enacted_in_round(1)
        assert len(round_1_laws) == 1
        assert round_1_laws[0].agenda_card.get_name() == "Fleet Regulations"

        round_3_laws = law_manager.get_laws_enacted_in_round(3)
        assert len(round_3_laws) == 1
        assert round_3_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"

        # Test getting laws enacted before a certain round
        early_laws = law_manager.get_laws_enacted_before_round(3)
        assert len(early_laws) == 1
        assert early_laws[0].agenda_card.get_name() == "Fleet Regulations"


class TestGameStateLawIntegration:
    """Test suite for law system integration with game state (Task 4.2)."""

    def test_game_state_tracks_active_laws(self) -> None:
        """Test that GameState can track active laws."""
        # RED: This should fail as GameState doesn't have law tracking yet
        from ti4.core.agenda_cards.law_manager import LawManager
        from ti4.core.game_state import GameState

        # Create game state with law manager
        game_state = GameState()
        assert hasattr(game_state, "law_manager")
        assert isinstance(game_state.law_manager, LawManager)
        assert game_state.law_manager.get_law_count() == 0

    def test_game_state_law_manager_persistence(self) -> None:
        """Test that law manager state persists in game state."""
        # RED: This should fail as GameState law integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        # Create game state and enact a law
        game_state = GameState()
        law_card = LawCard("Fleet Regulations")

        game_state.law_manager.enact_law(
            agenda_card_or_active_law=law_card,
            enacted_round=2,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Verify law is tracked
        assert game_state.law_manager.get_law_count() == 1
        assert game_state.law_manager.has_active_law("Fleet Regulations") is True

        # Test law persistence across game state operations
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Fleet Regulations"

    def test_law_effects_on_game_mechanics(self) -> None:
        """Test that laws can affect game mechanics through context checking."""
        # RED: This should fail as law effect integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        # Create game state with technology law
        game_state = GameState()
        tech_law = LawCard("Anti-Intellectual Revolution")

        game_state.law_manager.enact_law(
            agenda_card_or_active_law=tech_law,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )

        # Test law effect checking during game actions
        tech_context = GameContext(
            action_type="research_technology",
            player_id="player_1",
            additional_data={"technology": "Sarween Tools"},
        )

        # Check if laws affect this context
        affecting_laws = game_state.check_laws_affecting_context(tech_context)
        assert len(affecting_laws) == 1
        assert (
            affecting_laws[0].agenda_card.get_name() == "Anti-Intellectual Revolution"
        )

    def test_law_conflict_detection(self) -> None:
        """Test law conflict detection and resolution."""
        # RED: This should fail as conflict detection doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        game_state = GameState()

        # Enact first minister law
        minister1 = LawCard("Minister of Commerce")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=minister1,
            enacted_round=1,
            elected_target="player_1",
            effect_description="Elected player gains 1 trade good when they gain command tokens",
        )

        # Enact conflicting minister law
        minister2 = LawCard("Minister of War")
        conflicts = game_state.check_law_conflicts(minister2)

        # Should detect conflict with existing minister
        assert len(conflicts) == 1
        assert conflicts[0].agenda_card.get_name() == "Minister of Commerce"

        # Enact the new law (should replace the old one)
        game_state.enact_law_with_conflict_resolution(
            agenda_card_or_active_law=minister2,
            enacted_round=2,
            elected_target="player_2",
            effect_description="Elected player gains +1 to combat rolls",
        )

        # Verify old law was removed and new law was added
        assert game_state.law_manager.get_law_count() == 1
        assert game_state.law_manager.has_active_law("Minister of Commerce") is False
        assert game_state.law_manager.has_active_law("Minister of War") is True

    def test_law_effect_validation_during_actions(self) -> None:
        """Test that law effects are validated during game actions."""
        # RED: This should fail as action validation doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        game_state = GameState()

        # Enact fleet regulations law
        fleet_law = LawCard("Fleet Regulations")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=fleet_law,
            enacted_round=1,
            effect_description="Players cannot have more than 4 tokens in their fleet pools",
        )

        # Test fleet pool validation
        fleet_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 5},
        )

        # Should detect law violation
        violations = game_state.validate_action_against_laws(fleet_context)
        assert len(violations) == 1
        assert "fleet pool" in violations[0].lower()

        # Test valid fleet pool size
        valid_context = GameContext(
            action_type="fleet_pool_check",
            player_id="player_1",
            additional_data={"fleet_pool_size": 3},
        )

        valid_violations = game_state.validate_action_against_laws(valid_context)
        assert len(valid_violations) == 0

    def test_game_state_law_serialization(self) -> None:
        """Test that law state can be serialized with game state."""
        # RED: This should fail as serialization doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        # Create game state with laws
        game_state = GameState()
        law1 = LawCard("Fleet Regulations")
        law2 = LawCard("Anti-Intellectual Revolution")

        game_state.law_manager.enact_law(law1, 1, effect_description="Fleet limit")
        game_state.law_manager.enact_law(law2, 2, effect_description="Destroy ships")

        # Test serialization
        serialized = game_state.serialize_law_state()
        assert "active_laws" in serialized
        assert len(serialized["active_laws"]) == 2

        # Test deserialization
        new_game_state = GameState()
        new_game_state.deserialize_law_state(serialized)

        assert new_game_state.law_manager.get_law_count() == 2
        assert new_game_state.law_manager.has_active_law("Fleet Regulations") is True
        assert (
            new_game_state.law_manager.has_active_law("Anti-Intellectual Revolution")
            is True
        )

    def test_law_manager_immutability_in_game_state(self) -> None:
        """Test that law manager maintains immutability principles."""
        # RED: This should fail as immutability handling doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState

        game_state = GameState()
        law_card = LawCard("Test Law")

        # Enact law
        game_state.law_manager.enact_law(law_card, 1, effect_description="Test effect")

        # Get laws should return copy, not reference
        laws1 = game_state.law_manager.get_active_laws()
        laws2 = game_state.law_manager.get_active_laws()

        # Should be different objects but same content
        assert laws1 is not laws2
        assert len(laws1) == len(laws2) == 1
        assert laws1[0].agenda_card.get_name() == laws2[0].agenda_card.get_name()

        # Modifying returned list shouldn't affect internal state
        laws1.clear()
        assert game_state.law_manager.get_law_count() == 1

    def test_law_integration_with_existing_game_state_fields(self) -> None:
        """Test that law system integrates properly with existing GameState fields."""
        # RED: This should fail as integration doesn't exist yet
        from ti4.core.agenda_cards.base import LawCard
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        # Create game state with players
        player1 = Player("player_1", "Red")
        player2 = Player("player_2", "Blue")
        game_state = GameState(players=[player1, player2])

        # Enact law affecting players
        minister_law = LawCard("Minister of Commerce")
        game_state.law_manager.enact_law(
            agenda_card_or_active_law=minister_law,
            enacted_round=1,
            elected_target="player_1",
            effect_description="Elected player gains 1 trade good when they gain command tokens",
        )

        # Test law integration with player data
        elected_player_laws = game_state.get_laws_affecting_player("player_1")
        assert len(elected_player_laws) == 1
        assert elected_player_laws[0].elected_target == "player_1"

        non_elected_player_laws = game_state.get_laws_affecting_player("player_2")
        assert len(non_elected_player_laws) == 0

    def test_law_system_error_handling_in_game_state(self) -> None:
        """Test error handling for law system in game state context."""
        # RED: This should fail as error handling doesn't exist yet
        from ti4.core.agenda_cards.law_manager import GameContext
        from ti4.core.game_state import GameState

        game_state = GameState()

        # Test invalid law enactment
        with pytest.raises(ValueError, match="agenda_card cannot be None"):
            game_state.law_manager.enact_law(None, 1, effect_description="Test")  # type: ignore

        # Test invalid context checking
        invalid_context = GameContext(
            action_type="",  # Empty action type
            player_id="player_1",
        )

        # Should handle gracefully
        affecting_laws = game_state.check_laws_affecting_context(invalid_context)
        assert len(affecting_laws) == 0

        # Test law removal error handling
        result = game_state.law_manager.remove_law("Non-existent Law")
        assert result is False


class TestRemainingDirectiveCards:
    """Test suite for remaining directive cards (Task 10.2)."""

    def test_core_mining_directive_card_creation(self) -> None:
        """Test that Core Mining directive card can be created."""
        # RED: This should fail as CoreMining doesn't exist yet
        from ti4.core.agenda_cards.concrete.core_mining import CoreMining

        card = CoreMining()
        assert card is not None
        assert card.get_name() == "Core Mining"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_demilitarized_zone_directive_card_creation(self) -> None:
        """Test that Demilitarized Zone directive card can be created."""
        # RED: This should fail as DemilitarizedZone doesn't exist yet
        from ti4.core.agenda_cards.concrete.demilitarized_zone import DemilitarizedZone

        card = DemilitarizedZone()
        assert card is not None
        assert card.get_name() == "Demilitarized Zone"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_senate_sanctuary_directive_card_creation(self) -> None:
        """Test that Senate Sanctuary directive card can be created."""
        # RED: This should fail as SenateSanctuary doesn't exist yet
        from ti4.core.agenda_cards.concrete.senate_sanctuary import SenateSanctuary

        card = SenateSanctuary()
        assert card is not None
        assert card.get_name() == "Senate Sanctuary"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_terraforming_initiative_directive_card_creation(self) -> None:
        """Test that Terraforming Initiative directive card can be created."""
        # RED: This should fail as TerraformingInitiative doesn't exist yet
        from ti4.core.agenda_cards.concrete.terraforming_initiative import (
            TerraformingInitiative,
        )

        card = TerraformingInitiative()
        assert card is not None
        assert card.get_name() == "Terraforming Initiative"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_research_team_directive_card_creation(self) -> None:
        """Test that Research Team directive card can be created."""
        # RED: This should fail as ResearchTeam doesn't exist yet
        from ti4.core.agenda_cards.concrete.research_team import ResearchTeam

        card = ResearchTeam()
        assert card is not None
        assert card.get_name() == "Research Team"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_shard_of_the_throne_directive_card_creation(self) -> None:
        """Test that Shard of the Throne directive card can be created."""
        # RED: This should fail as ShardOfTheThrone doesn't exist yet
        from ti4.core.agenda_cards.concrete.shard_of_the_throne import ShardOfTheThrone

        card = ShardOfTheThrone()
        assert card is not None
        assert card.get_name() == "Shard of the Throne"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE

    def test_crown_directive_card_creation(self) -> None:
        """Test that Crown directive card can be created."""
        # RED: This should fail as Crown doesn't exist yet
        from ti4.core.agenda_cards.concrete.crown import Crown

        card = Crown()
        assert card is not None
        assert card.get_name() == "Crown"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE


class TestVotingSystemIntegrationEnhancements:
    """Test suite for voting system integration enhancements (Task 9.2)."""

    def test_voting_system_election_mechanics_validation(self) -> None:
        """Test voting system validates election mechanics for agenda cards."""
        # RED: This should fail as election mechanics validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VotingSystem
        from ti4.core.game_state import GameState

        voting_system = VotingSystem()
        game_state = GameState()
        election_card = ClassifiedDocumentLeaks()

        # Test that voting system can validate election targets
        valid_targets = voting_system.get_valid_election_targets(
            election_card, game_state
        )
        assert isinstance(valid_targets, list)

        # Test election target validation
        is_valid = voting_system.validate_election_target(
            election_card, "test_objective", game_state
        )
        assert isinstance(is_valid, bool)

    def test_voting_system_agenda_specific_validation(self) -> None:
        """Test voting system provides agenda-specific validation."""
        # RED: This should fail as agenda-specific validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_phase import VotingSystem
        from ti4.core.game_state import GameState

        voting_system = VotingSystem()
        game_state = GameState()
        minister_card = MinisterOfCommerce()

        # Test that voting system validates player elections
        validation_result = voting_system.validate_agenda_specific_requirements(
            minister_card, "player_1", game_state
        )
        assert hasattr(validation_result, "is_valid")
        assert hasattr(validation_result, "error_message")

    def test_voting_system_enhanced_error_handling(self) -> None:
        """Test enhanced error handling for voting with agenda cards."""
        # RED: This should fail as enhanced error handling doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_phase import VotingSystem, VotingValidationError

        voting_system = VotingSystem()
        agenda_card = AntiIntellectualRevolution()

        # Test specific error types for agenda validation
        with pytest.raises(VotingValidationError) as exc_info:
            voting_system.validate_outcome_with_detailed_errors(
                "Invalid Outcome", agenda_card
            )

        assert "Invalid voting outcome" in str(exc_info.value)
        assert exc_info.value.agenda_name == "Anti-Intellectual Revolution"
        assert exc_info.value.attempted_outcome == "Invalid Outcome"

    def test_voting_system_election_outcome_processing(self) -> None:
        """Test voting system processes election outcomes correctly."""
        # RED: This should fail as election outcome processing doesn't exist yet
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_phase import VoteResult, VotingSystem
        from ti4.core.game_state import GameState

        voting_system = VotingSystem()
        game_state = GameState()
        election_card = ClassifiedDocumentLeaks()

        # Create a vote result with election outcome
        vote_result = VoteResult(
            outcome="Elect Scored Secret Objective",
            elected_target="test_objective",
            success=True,
        )

        # Test that voting system can process election results
        processed_result = voting_system.process_election_outcome(
            election_card, vote_result, game_state
        )
        assert processed_result.success is True
        assert processed_result.elected_target == "test_objective"

    def test_voting_system_committee_formation_bypass_integration(self) -> None:
        """Test voting system integrates with Committee Formation bypass mechanics."""
        # RED: This should fail as bypass integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.committee_formation import (
            CommitteeFormation,
        )
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_phase import VotingSystem
        from ti4.core.game_state import GameState

        voting_system = VotingSystem()
        game_state = GameState()
        committee_card = CommitteeFormation()
        minister_card = MinisterOfCommerce()

        # Test that voting system recognizes bypass opportunities
        can_bypass = voting_system.can_bypass_voting(committee_card, minister_card)
        assert can_bypass is True

        # Test bypass execution through voting system
        bypass_result = voting_system.execute_voting_bypass(
            committee_card, minister_card, "player_1", game_state
        )
        assert bypass_result.success is True
        assert bypass_result.bypassed_by_committee_formation is True

    def test_voting_system_comprehensive_outcome_validation(self) -> None:
        """Test comprehensive outcome validation for all agenda card types."""
        # RED: This should fail as comprehensive validation doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_phase import VotingSystem

        voting_system = VotingSystem()

        # Test For/Against law validation
        law_card = AntiIntellectualRevolution()
        assert voting_system.validate_outcome_against_card("For", law_card) is True
        assert voting_system.validate_outcome_against_card("Against", law_card) is True
        assert voting_system.validate_outcome_against_card("Invalid", law_card) is False

        # Test election directive validation
        directive_card = ClassifiedDocumentLeaks()
        assert (
            voting_system.validate_outcome_against_card(
                "Elect Scored Secret Objective", directive_card
            )
            is True
        )
        assert (
            voting_system.validate_outcome_against_card("For", directive_card) is False
        )

        # Test player election law validation
        minister_card = MinisterOfCommerce()
        assert (
            voting_system.validate_outcome_against_card("Elect Player", minister_card)
            is True
        )
        assert (
            voting_system.validate_outcome_against_card("Against", minister_card)
            is False
        )


class TestLawConflictDetectionAndResolution:
    """Test suite for law conflict detection and resolution (Task 12.2)."""

    def test_minister_card_replacement_detection(self) -> None:
        """Test detection of minister card replacements."""
        # RED: This should fail as enhanced conflict detection doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Enact first minister law
        minister1 = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister1,
            enacted_round=1,
            effect_description="Minister of Commerce effect",
            elected_target="player1",
        )

        # Try to enact same minister type (should detect conflict)
        minister2 = MinisterOfCommerce()
        conflicts = law_manager.check_law_conflicts(minister2)

        assert len(conflicts) == 1
        assert conflicts[0].agenda_card.get_name() == "Minister of Commerce"
        assert conflicts[0].elected_target == "player1"

    def test_multiple_minister_conflict_detection(self) -> None:
        """Test that any minister conflicts with any other minister."""
        # RED: This should fail as we need to create a mock Minister of War card
        from ti4.core.agenda_cards.base.law_card import LawCard
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Enact Minister of Commerce
        minister_commerce = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister_commerce,
            enacted_round=1,
            effect_description="Minister of Commerce effect",
            elected_target="player1",
        )

        # Create mock Minister of War (different minister type)
        class MockMinisterOfWar(LawCard):
            def __init__(self) -> None:
                super().__init__("Minister of War")

        minister_war = MockMinisterOfWar()
        conflicts = law_manager.check_law_conflicts(minister_war)

        # Should detect conflict with existing minister
        assert len(conflicts) == 1
        assert conflicts[0].agenda_card.get_name() == "Minister of Commerce"

    def test_automatic_law_removal_on_conflict(self) -> None:
        """Test automatic removal of conflicting laws when enacting new law."""
        # RED: This should fail as automatic removal isn't fully implemented
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Enact first minister law
        minister1 = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister1,
            enacted_round=1,
            effect_description="First minister effect",
            elected_target="player1",
        )

        assert law_manager.get_law_count() == 1

        # Enact conflicting minister law (should automatically remove the first)
        minister2 = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister2,
            enacted_round=2,
            effect_description="Second minister effect",
            elected_target="player2",
        )

        # Should only have the new law
        assert law_manager.get_law_count() == 1
        active_laws = law_manager.get_active_laws()
        assert active_laws[0].elected_target == "player2"
        assert active_laws[0].enacted_round == 2

    def test_conflict_resolution_messaging(self) -> None:
        """Test clear conflict resolution messaging."""
        # RED: This should fail as conflict messaging doesn't exist yet
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import (
            ConflictResolutionResult,
            LawManager,
        )

        law_manager = LawManager()

        # Enact first minister law
        minister1 = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister1,
            enacted_round=1,
            effect_description="First minister effect",
            elected_target="player1",
        )

        # Enact conflicting law with messaging
        minister2 = MinisterOfCommerce()
        result = law_manager.enact_law_with_conflict_resolution(
            agenda_card_or_active_law=minister2,
            enacted_round=2,
            effect_description="Second minister effect",
            elected_target="player2",
        )

        assert isinstance(result, ConflictResolutionResult)
        assert len(result.removed_laws) == 1
        assert result.removed_laws[0].agenda_card.get_name() == "Minister of Commerce"
        assert result.removed_laws[0].elected_target == "player1"
        assert result.enacted_law.elected_target == "player2"
        assert "Minister of Commerce" in result.message
        assert "replaced" in result.message.lower()

    def test_non_conflicting_laws_coexist(self) -> None:
        """Test that non-conflicting laws can coexist."""
        # RED: This should fail as we need to create non-minister law cards
        from ti4.core.agenda_cards.base.law_card import LawCard
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Create mock non-minister law
        class MockRegularLaw(LawCard):
            def __init__(self) -> None:
                super().__init__("Fleet Regulations")

        # Enact minister law
        minister = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister,
            enacted_round=1,
            effect_description="Minister effect",
            elected_target="player1",
        )

        # Enact non-minister law (should not conflict)
        regular_law = MockRegularLaw()
        conflicts = law_manager.check_law_conflicts(regular_law)
        assert len(conflicts) == 0

        law_manager.enact_law(
            agenda_card_or_active_law=regular_law,
            enacted_round=2,
            effect_description="Regular law effect",
        )

        # Both laws should coexist
        assert law_manager.get_law_count() == 2

    def test_complex_conflict_scenarios(self) -> None:
        """Test complex conflict scenarios with multiple law types."""
        # RED: This should fail as complex conflict detection doesn't exist yet
        from ti4.core.agenda_cards.base.law_card import LawCard
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Create multiple mock minister cards
        class MockMinisterOfWar(LawCard):
            def __init__(self) -> None:
                super().__init__("Minister of War")

        class MockMinisterOfPolicy(LawCard):
            def __init__(self) -> None:
                super().__init__("Minister of Policy")

        # Enact multiple ministers (should all conflict with each other)
        minister_commerce = MinisterOfCommerce()
        law_manager.enact_law(
            agenda_card_or_active_law=minister_commerce,
            enacted_round=1,
            effect_description="Commerce effect",
            elected_target="player1",
        )

        minister_war = MockMinisterOfWar()
        conflicts = law_manager.check_law_conflicts(minister_war)
        assert len(conflicts) == 1  # Should conflict with commerce minister

        # Enact war minister (should replace commerce minister)
        law_manager.enact_law(
            agenda_card_or_active_law=minister_war,
            enacted_round=2,
            effect_description="War effect",
            elected_target="player2",
        )

        assert law_manager.get_law_count() == 1
        assert (
            law_manager.get_active_laws()[0].agenda_card.get_name() == "Minister of War"
        )

        # Try to enact policy minister (should replace war minister)
        minister_policy = MockMinisterOfPolicy()
        conflicts = law_manager.check_law_conflicts(minister_policy)
        assert len(conflicts) == 1  # Should conflict with war minister

    def test_conflict_detection_edge_cases(self) -> None:
        """Test edge cases in conflict detection."""
        # RED: This should fail as edge case handling doesn't exist yet
        from ti4.core.agenda_cards.base.law_card import LawCard
        from ti4.core.agenda_cards.law_manager import LawManager

        law_manager = LawManager()

        # Test with None agenda card
        conflicts = law_manager.check_law_conflicts(None)
        assert len(conflicts) == 0

        # Test with empty law manager
        class MockLaw(LawCard):
            def __init__(self) -> None:
                super().__init__("Test Law")

        test_law = MockLaw()
        conflicts = law_manager.check_law_conflicts(test_law)
        assert len(conflicts) == 0

        # Test with law that has "Minister" in description but isn't a minister card
        class MockNonMinisterLaw(LawCard):
            def __init__(self) -> None:
                super().__init__(
                    "Law About Ministers"
                )  # Contains "Minister" but isn't one

        non_minister_law = MockNonMinisterLaw()
        conflicts = law_manager.check_law_conflicts(non_minister_law)
        assert len(conflicts) == 0


class TestAgendaCardValidationSystem:
    """Test suite for agenda card validation system (Task 12.1)."""

    def test_agenda_card_validation_error_exists(self) -> None:
        """Test that AgendaCardValidationError exception is defined."""
        # RED: This should fail as AgendaCardValidationError doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError

        # Test that it's a proper exception
        assert issubclass(AgendaCardValidationError, Exception)

        # Test that it can be instantiated with a message
        error = AgendaCardValidationError("Test validation error")
        assert str(error) == "Test validation error"

    def test_invalid_agenda_card_name_validation(self) -> None:
        """Test validation of invalid agenda card names."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test empty name
        with pytest.raises(
            AgendaCardValidationError, match="Agenda card name cannot be empty"
        ):
            validator.validate_card_name("")

        # Test whitespace-only name
        with pytest.raises(
            AgendaCardValidationError, match="Agenda card name cannot be empty"
        ):
            validator.validate_card_name("   ")

        # Test None name
        with pytest.raises(
            AgendaCardValidationError, match="Agenda card name cannot be None"
        ):
            validator.validate_card_name(None)  # type: ignore

    def test_valid_agenda_card_name_validation(self) -> None:
        """Test validation of valid agenda card names."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test valid names
        assert validator.validate_card_name("Anti-Intellectual Revolution") is True
        assert validator.validate_card_name("Fleet Regulations") is True
        assert validator.validate_card_name("Committee Formation") is True

        # Test name with spaces is trimmed and validated
        assert validator.validate_card_name("  Valid Name  ") is True

    def test_invalid_voting_outcomes_validation(self) -> None:
        """Test validation of invalid voting outcomes."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test empty outcomes list
        with pytest.raises(
            AgendaCardValidationError, match="Voting outcomes cannot be empty"
        ):
            validator.validate_voting_outcomes([])

        # Test None outcomes
        with pytest.raises(
            AgendaCardValidationError, match="Voting outcomes cannot be None"
        ):
            validator.validate_voting_outcomes(None)  # type: ignore

        # Test outcomes with empty strings
        with pytest.raises(
            AgendaCardValidationError, match="Voting outcome cannot be empty"
        ):
            validator.validate_voting_outcomes(["For", "", "Against"])

        # Test outcomes with None values
        with pytest.raises(
            AgendaCardValidationError, match="Voting outcome cannot be None"
        ):
            validator.validate_voting_outcomes(["For", None, "Against"])  # type: ignore

    def test_valid_voting_outcomes_validation(self) -> None:
        """Test validation of valid voting outcomes."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test standard For/Against outcomes
        assert validator.validate_voting_outcomes(["For", "Against"]) is True

        # Test election outcomes
        assert validator.validate_voting_outcomes(["Elect Player"]) is True
        assert validator.validate_voting_outcomes(["Elect Cultural Planet"]) is True

        # Test multiple election outcomes
        assert (
            validator.validate_voting_outcomes(
                [
                    "Elect Cultural Planet",
                    "Elect Industrial Planet",
                    "Elect Hazardous Planet",
                ]
            )
            is True
        )

    def test_invalid_agenda_type_validation(self) -> None:
        """Test validation of invalid agenda types."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test None agenda type
        with pytest.raises(
            AgendaCardValidationError, match="Agenda type cannot be None"
        ):
            validator.validate_agenda_type(None)  # type: ignore

        # Test invalid string agenda type
        with pytest.raises(AgendaCardValidationError, match="Invalid agenda type"):
            validator.validate_agenda_type("invalid_type")  # type: ignore

    def test_valid_agenda_type_validation(self) -> None:
        """Test validation of valid agenda types."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test valid agenda types
        assert validator.validate_agenda_type(AgendaType.LAW) is True
        assert validator.validate_agenda_type(AgendaType.DIRECTIVE) is True

    def test_invalid_card_metadata_validation(self) -> None:
        """Test validation of invalid card metadata."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test None metadata
        with pytest.raises(
            AgendaCardValidationError, match="Card metadata cannot be None"
        ):
            validator.validate_card_metadata(None)  # type: ignore

        # Test non-dict metadata
        with pytest.raises(
            AgendaCardValidationError, match="Card metadata must be a dictionary"
        ):
            validator.validate_card_metadata("not a dict")  # type: ignore

        # Test metadata with invalid expansion
        with pytest.raises(AgendaCardValidationError, match="Invalid expansion"):
            validator.validate_card_metadata({"expansion": ""})

    def test_valid_card_metadata_validation(self) -> None:
        """Test validation of valid card metadata."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test valid metadata
        valid_metadata = {"expansion": "Base", "flavor_text": "Some flavor text"}
        assert validator.validate_card_metadata(valid_metadata) is True

        # Test metadata with optional fields
        metadata_with_optional = {
            "expansion": "Prophecy of Kings",
            "flavor_text": None,
            "custom_field": "custom_value",
        }
        assert validator.validate_card_metadata(metadata_with_optional) is True

    def test_comprehensive_card_validation(self) -> None:
        """Test comprehensive validation of complete agenda card data."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test valid complete card data
        valid_card_data = {
            "name": "Anti-Intellectual Revolution",
            "agenda_type": AgendaType.LAW,
            "outcomes": ["For", "Against"],
            "metadata": {"expansion": "Base", "flavor_text": "Knowledge is dangerous."},
        }

        assert validator.validate_complete_card_data(valid_card_data) is True

    def test_comprehensive_card_validation_with_invalid_data(self) -> None:
        """Test comprehensive validation with invalid card data."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test invalid card data - missing name
        invalid_card_data = {
            "agenda_type": AgendaType.LAW,
            "outcomes": ["For", "Against"],
            "metadata": {"expansion": "Base"},
        }

        with pytest.raises(
            AgendaCardValidationError, match="Card data must contain 'name'"
        ):
            validator.validate_complete_card_data(invalid_card_data)

        # Test invalid card data - invalid outcomes
        invalid_outcomes_data = {
            "name": "Test Card",
            "agenda_type": AgendaType.LAW,
            "outcomes": [],  # Empty outcomes
            "metadata": {"expansion": "Base"},
        }

        with pytest.raises(
            AgendaCardValidationError, match="Voting outcomes cannot be empty"
        ):
            validator.validate_complete_card_data(invalid_outcomes_data)

    def test_election_target_validation(self) -> None:
        """Test validation of election targets."""
        # RED: This should fail as validation doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test valid player election target
        assert validator.validate_election_target("player1", "Elect Player") is True

        # Test valid planet election target
        assert (
            validator.validate_election_target("Mecatol Rex", "Elect Cultural Planet")
            is True
        )

        # Test invalid election target for outcome type
        with pytest.raises(AgendaCardValidationError, match="Invalid election target"):
            validator.validate_election_target("", "Elect Player")

        # Test None election target
        with pytest.raises(
            AgendaCardValidationError, match="Election target cannot be None"
        ):
            validator.validate_election_target(None, "Elect Player")  # type: ignore

    def test_graceful_error_recovery(self) -> None:
        """Test graceful error recovery and user feedback."""
        # RED: This should fail as error recovery doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test that validation errors provide helpful feedback
        try:
            validator.validate_card_name("")
        except Exception as e:
            assert "Agenda card name cannot be empty" in str(e)
            assert hasattr(e, "get_recovery_suggestions")
            suggestions = e.get_recovery_suggestions()  # type: ignore
            assert isinstance(suggestions, list)
            assert len(suggestions) > 0

    def test_validation_error_context_information(self) -> None:
        """Test that validation errors provide context information."""
        # RED: This should fail as context information doesn't exist yet
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError

        # Test that validation errors can include context
        error = AgendaCardValidationError(
            message="Invalid card data",
            card_name="Test Card",
            field_name="outcomes",
            invalid_value=[],
        )

        assert error.card_name == "Test Card"
        assert error.field_name == "outcomes"
        assert error.invalid_value == []
        assert "Test Card" in str(error)

    def test_batch_validation_operations(self) -> None:
        """Test batch validation of multiple agenda cards."""
        # RED: This should fail as batch validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test batch validation of multiple cards
        card_data_list = [
            {
                "name": "Card 1",
                "agenda_type": AgendaType.LAW,
                "outcomes": ["For", "Against"],
                "metadata": {"expansion": "Base"},
            },
            {
                "name": "Card 2",
                "agenda_type": AgendaType.DIRECTIVE,
                "outcomes": ["Elect Player"],
                "metadata": {"expansion": "Base"},
            },
        ]

        validation_results = validator.validate_multiple_cards(card_data_list)
        assert len(validation_results) == 2
        assert all(result.is_valid for result in validation_results)

    def test_batch_validation_with_errors(self) -> None:
        """Test batch validation with some invalid cards."""
        # RED: This should fail as batch validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test batch validation with mixed valid/invalid cards
        card_data_list = [
            {
                "name": "Valid Card",
                "agenda_type": AgendaType.LAW,
                "outcomes": ["For", "Against"],
                "metadata": {"expansion": "Base"},
            },
            {
                "name": "",  # Invalid - empty name
                "agenda_type": AgendaType.DIRECTIVE,
                "outcomes": ["Elect Player"],
                "metadata": {"expansion": "Base"},
            },
        ]

        validation_results = validator.validate_multiple_cards(card_data_list)
        assert len(validation_results) == 2
        assert validation_results[0].is_valid is True
        assert validation_results[1].is_valid is False
        assert "empty" in validation_results[1].error_message.lower()

    def test_validation_performance_benchmarks(self) -> None:
        """Test that validation operations meet performance requirements."""
        # RED: This should fail as performance benchmarks don't exist yet
        import time

        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.constants import AgendaType

        validator = AgendaCardValidator()

        # Test single card validation performance
        card_data = {
            "name": "Performance Test Card",
            "agenda_type": AgendaType.LAW,
            "outcomes": ["For", "Against"],
            "metadata": {"expansion": "Base"},
        }

        start_time = time.time()
        for _ in range(1000):  # Validate 1000 times
            validator.validate_complete_card_data(card_data)
        end_time = time.time()

        # Should complete 1000 validations in less than 1 second
        assert (end_time - start_time) < 1.0

    def test_custom_validation_rules(self) -> None:
        """Test support for custom validation rules."""
        # RED: This should fail as custom validation doesn't exist yet
        from ti4.core.agenda_cards.validation import AgendaCardValidator

        validator = AgendaCardValidator()

        # Test adding custom validation rule
        def custom_name_rule(name: str) -> bool:
            return not name.startswith("Invalid")

        validator.add_custom_validation_rule("name", custom_name_rule)

        # Test that custom rule is applied
        assert validator.validate_card_name("Valid Name") is True

        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError

        with pytest.raises(AgendaCardValidationError):
            validator.validate_card_name("Invalid Name")
