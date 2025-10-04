"""
Tests for agenda card system integration with existing game systems (Task 13.2).

This module tests the integration of agenda card effects with movement, production,
combat systems, and technology research.
"""


class TestAgendaCardSystemIntegration:
    """Test suite for agenda card integration with existing game systems (Task 13.2)."""

    def test_anti_intellectual_revolution_technology_research_integration(self) -> None:
        """Test Anti-Intellectual Revolution law affects technology research."""
        # RED: This should fail as technology research integration doesn't exist yet
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw

        # Create game state with player and ships
        from ti4.core.constants import Faction, Technology, UnitType
        from ti4.core.game_state import GameState
        from ti4.core.player import Player
        from ti4.core.technology import TechnologyManager
        from ti4.core.unit import Unit

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

        # Create game state with player
        from ti4.core.constants import Faction
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

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

        # Create game state with player and planet
        from ti4.core.constants import Faction, UnitType
        from ti4.core.game_state import GameState
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.production import ProductionManager
        from ti4.core.unit import Unit

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

        # Create game state with player and galaxy
        from ti4.core.constants import Faction, UnitType
        from ti4.core.galaxy import Galaxy
        from ti4.core.game_state import GameState
        from ti4.core.movement import MovementOperation, MovementValidator
        from ti4.core.player import Player
        from ti4.core.unit import Unit

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

        # Create game state with players
        from ti4.core.constants import Faction, UnitType
        from ti4.core.game_state import GameState
        from ti4.core.player import Player
        from ti4.core.unit import Unit

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

        # Create game state with multiple active laws
        from ti4.core.constants import Faction
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

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
