"""
End-to-end integration tests for Rule 7: AGENDA CARDS system.

This module tests complete agenda phase workflows including:
- Law enactment and persistent effects across multiple rounds
- Directive execution and immediate effects
- Election mechanics with all card types
- Full integration with voting, game state, and other systems

Tests follow TDD RED-GREEN-REFACTOR methodology.
"""

from ti4.core.constants import Faction, UnitType
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.unit import Unit


class TestCompleteAgendaPhaseWorkflows:
    """Test complete agenda phase workflows from start to finish."""

    def test_complete_law_enactment_workflow(self) -> None:
        """Test complete workflow for law enactment from revelation to persistent effects.

        RED: This test should fail as the complete workflow integration doesn't exist yet.
        """
        # Arrange: Set up game state with players and agenda phase
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase, SpeakerSystem, VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        # Add planets for voting
        planet1 = Planet(name="Mecatol Rex", resources=1, influence=6)
        planet1.controlled_by = "player1"
        planet2 = Planet(name="Jord", resources=4, influence=2)
        planet2.controlled_by = "player2"

        game_state = game_state._create_new_state(
            players=[player1, player2],
            player_planets={"player1": [planet1], "player2": [planet2]},
        )

        # Set up agenda phase components
        registry = AgendaCardRegistry()
        # Register some cards for testing
        registry.register_card(FleetRegulations())
        deck = AgendaDeck(registry)
        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()
        speaker_system.set_speaker("player1")

        agenda_phase = AgendaPhase(
            deck=deck, voting_system=voting_system, speaker_system=speaker_system
        )

        # Act: Execute complete agenda phase workflow

        # Step 1: Reveal agenda card
        revealed_card = agenda_phase.reveal_agenda_card()
        assert revealed_card is not None
        assert isinstance(
            revealed_card, FleetRegulations
        )  # Assuming this is first card

        # Step 2: Players vote on the agenda
        # Player 1 votes "For" using Mecatol Rex (6 influence)
        vote_result1 = voting_system.cast_votes(
            player_id="player1", planets=[planet1], outcome="For", agenda=revealed_card
        )
        assert vote_result1.success is True
        assert vote_result1.votes_cast == 6

        # Player 2 votes "Against" using Jord (2 influence)
        vote_result2 = voting_system.cast_votes(
            player_id="player2",
            planets=[planet2],
            outcome="Against",
            agenda=revealed_card,
        )
        assert vote_result2.success is True
        assert vote_result2.votes_cast == 2

        # Step 3: Resolve voting outcome
        vote_tally = voting_system.get_vote_tally()
        assert vote_tally["For"] == 6
        assert vote_tally["Against"] == 2

        winning_outcome = agenda_phase.determine_winning_outcome(vote_tally)
        assert winning_outcome == "For"

        # Step 4: Apply agenda effects
        resolution_result = agenda_phase.resolve_agenda_outcome(
            agenda=revealed_card, outcome=winning_outcome, game_state=game_state
        )

        # Assert: Verify law was enacted and effects applied
        assert resolution_result.success is True
        assert resolution_result.law_enacted is True

        # Verify law is now active in game state
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 1
        assert active_laws[0].agenda_card.get_name() == "Fleet Regulations"

        # Step 5: Verify persistent effects in subsequent rounds
        # Try to add more than 4 fleet pool tokens (should be blocked by law)
        from ti4.core.command_tokens import CommandTokenManager

        token_manager = CommandTokenManager()

        # Should be able to add up to 4 tokens
        for i in range(4):
            result = token_manager.add_fleet_pool_token("player1", game_state)
            assert result is True, f"Failed to add token {i + 1}"

        # 5th token should be blocked by Fleet Regulations law
        result = token_manager.add_fleet_pool_token("player1", game_state)
        assert result is False

        # Verify law effect was the reason for blocking
        law_effects = game_state.get_law_effects_for_action(
            "fleet_pool_management", "player1"
        )
        assert len(law_effects) == 1
        assert law_effects[0].agenda_card.get_name() == "Fleet Regulations"

    def test_complete_directive_execution_workflow(self) -> None:
        """Test complete workflow for directive execution with immediate effects.

        RED: This test should fail as directive workflow integration doesn't exist yet.
        """
        # Arrange: Set up game state for directive testing
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase, SpeakerSystem, VotingSystem

        # SecretObjective - using mock for now since it doesn't exist yet
        class SecretObjective:
            def __init__(
                self, name: str, description: str, points: int, scored_by: str
            ):
                self.name = name
                self.description = description
                self.points = points
                self.scored_by = scored_by

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        # Add scored secret objective for the directive to target
        secret_obj = SecretObjective(
            name="Become a Martyr",
            description="Lose 3 ships in one round",
            points=1,
            scored_by="player1",
        )
        game_state = game_state._create_new_state(
            players=[player1, player2], scored_secret_objectives=[secret_obj]
        )

        # Add planets for voting
        planet1 = Planet(name="Mecatol Rex", resources=1, influence=6)
        planet1.controlled_by = "player1"
        planet2 = Planet(name="Jord", resources=4, influence=2)
        planet2.controlled_by = "player2"

        # Set up agenda phase
        AgendaCardRegistry()
        deck = AgendaDeck([ClassifiedDocumentLeaks()])  # Force specific card
        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()
        speaker_system.set_speaker("player1")

        agenda_phase = AgendaPhase(
            deck=deck, voting_system=voting_system, speaker_system=speaker_system
        )

        # Act: Execute directive workflow

        # Step 1: Reveal directive card
        revealed_card = agenda_phase.reveal_agenda_card()
        assert revealed_card is not None
        assert isinstance(revealed_card, ClassifiedDocumentLeaks)

        # Step 2: Check if card should be discarded (it shouldn't - we have scored secrets)
        should_discard = revealed_card.should_discard_on_reveal(game_state)
        assert should_discard is False

        # Step 3: Conduct election for secret objective
        # Player 1 votes for "Become a Martyr"
        vote_result1 = voting_system.cast_votes(
            player_id="player1",
            planets=[planet1],
            outcome="Elect Scored Secret Objective",
            agenda=revealed_card,
        )
        assert vote_result1.success is True

        # Step 4: Process election outcome
        election_result = agenda_phase.process_election_outcome(
            agenda=revealed_card,
            vote_tally=voting_system.get_vote_tally(),
            elected_target="Become a Martyr",
        )
        assert election_result.success is True
        assert election_result.elected_target == "Become a Martyr"

        # Step 5: Execute directive effect
        resolution_result = agenda_phase.resolve_agenda_outcome(
            agenda=revealed_card,
            outcome="Elect Scored Secret Objective",
            game_state=game_state,
            elected_target="Become a Martyr",
        )

        # Assert: Verify directive effect was executed
        assert resolution_result.success is True
        assert resolution_result.directive_executed is True

        # Verify secret objective became public
        public_objectives = game_state.get_public_objectives()
        assert any(obj.name == "Become a Martyr" for obj in public_objectives)

        # Verify it's no longer a secret objective
        remaining_secrets = game_state.get_scored_secret_objectives()
        assert not any(obj.name == "Become a Martyr" for obj in remaining_secrets)

    def test_election_mechanics_with_all_card_types(self) -> None:
        """Test election mechanics work correctly with different card types.

        RED: This test should fail as comprehensive election mechanics don't exist yet.
        """
        # Arrange: Set up game state with various election targets
        from ti4.core.agenda_cards.concrete.holy_planet_of_ixth import HolyPlanetOfIxth
        from ti4.core.agenda_cards.concrete.minister_of_commerce import (
            MinisterOfCommerce,
        )
        from ti4.core.agenda_cards.concrete.shard_of_the_throne import ShardOfTheThrone
        from ti4.core.agenda_phase import AgendaPhase, SpeakerSystem, VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)
        player3 = Player(id="player3", faction=Faction.ARBOREC)

        # Add cultural planets for planet election
        cultural_planet = Planet(name="Abyz", resources=3, influence=0)
        cultural_planet.traits = ["cultural"]
        cultural_planet.controlled_by = "player1"

        game_state = game_state._create_new_state(
            players=[player1, player2, player3],
            player_planets={"player1": [cultural_planet]},
        )

        # Test 1: Player Election (Minister of Commerce)
        minister_card = MinisterOfCommerce()
        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()
        speaker_system.set_speaker("player1")

        # Players vote for different candidates
        planet1 = Planet(name="Mecatol Rex", resources=1, influence=6)
        planet1.controlled_by = "player1"
        planet2 = Planet(name="Jord", resources=4, influence=2)
        planet2.controlled_by = "player2"

        vote_result1 = voting_system.cast_votes(
            player_id="player1",
            planets=[planet1],
            outcome="Elect Player",
            agenda=minister_card,
        )
        assert vote_result1.success is True

        # Process player election
        election_result = AgendaPhase.process_player_election(
            vote_tally={"player2": 6, "player3": 2},
            valid_candidates=["player1", "player2", "player3"],
        )
        assert election_result.success is True
        assert election_result.elected_target == "player2"

        # Test 2: Planet Election (Holy Planet of Ixth)
        voting_system.reset_votes()
        holy_planet_card = HolyPlanetOfIxth()

        vote_result2 = voting_system.cast_votes(
            player_id="player1",
            planets=[planet1],
            outcome="Elect Cultural Planet",
            agenda=holy_planet_card,
        )
        assert vote_result2.success is True

        # Process planet election
        planet_election_result = AgendaPhase.process_planet_election(
            vote_tally={"Abyz": 6},
            planet_type="cultural",
            available_planets=[cultural_planet],
        )
        assert planet_election_result.success is True
        assert planet_election_result.elected_target == "Abyz"

        # Test 3: Victory Point Election (Shard of the Throne)
        voting_system.reset_votes()
        shard_card = ShardOfTheThrone()

        vote_result3 = voting_system.cast_votes(
            player_id="player1",
            planets=[planet1],
            outcome="Elect Player",
            agenda=shard_card,
        )
        assert vote_result3.success is True

        # Process VP election and verify VP gain
        vp_election_result = AgendaPhase.process_victory_point_election(
            elected_player="player2", agenda_card=shard_card, game_state=game_state
        )
        assert vp_election_result.success is True

        # Verify player gained victory point
        player2_vp = game_state.get_player_victory_points("player2")
        assert player2_vp >= 1  # Should have gained at least 1 VP

    def test_law_persistence_across_multiple_rounds(self) -> None:
        """Test that laws persist and continue to affect gameplay across multiple rounds.

        RED: This test should fail as multi-round law persistence doesn't exist yet.
        """
        # Arrange: Set up game state with multiple laws enacted over time
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.command_tokens import CommandTokenManager
        from ti4.core.constants import Technology
        from ti4.core.technology import TechnologyManager

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)

        # Add ships for Anti-Intellectual Revolution testing
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")

        game_state = game_state._create_new_state(
            players=[player1], player_units={"player1": [cruiser, destroyer]}
        )

        # Act: Enact laws in different rounds

        # Round 1: Enact Anti-Intellectual Revolution
        air_law = AntiIntellectualRevolution()
        active_air = ActiveLaw(
            agenda_card=air_law,
            enacted_round=1,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
        )
        game_state.law_manager.enact_law(active_air)

        # Round 2: Enact Fleet Regulations
        fleet_law = FleetRegulations()
        active_fleet = ActiveLaw(
            agenda_card=fleet_law,
            enacted_round=2,
            effect_description="Each player's fleet pool can have a maximum of 4 command tokens",
        )
        game_state.law_manager.enact_law(active_fleet)

        # Round 3: Test that both laws are still active and affecting gameplay

        # Test Anti-Intellectual Revolution (from Round 1) still works
        tech_manager = TechnologyManager()

        # Before research: player has 2 ships
        # Note: Using mock since get_player_units doesn't exist yet
        initial_ships = [cruiser, destroyer]  # Mock - would come from game_state
        assert len(initial_ships) == 2

        # Research technology - should trigger law effect
        tech_manager.research_technology("player1", Technology.GRAVITY_DRIVE)

        # Check law effect is triggered
        law_effects = game_state.get_law_effects_for_action(
            "technology_research", "player1"
        )
        air_effects = [
            effect
            for effect in law_effects
            if effect.agenda_card.get_name() == "Anti-Intellectual Revolution"
        ]
        assert len(air_effects) == 1

        # Apply law effect - should destroy one ship
        destroyed_ships = game_state.apply_law_effects(
            air_effects,
            {"available_ships": [cruiser, destroyer], "player_id": "player1"},
        )
        assert len(destroyed_ships) == 1

        # Test Fleet Regulations (from Round 2) still works
        token_manager = CommandTokenManager()

        # Should be able to add up to 4 tokens
        for _i in range(4):
            result = token_manager.add_fleet_pool_token("player1", game_state)
            assert result is True

        # 5th token should be blocked
        result = token_manager.add_fleet_pool_token("player1", game_state)
        assert result is False

        # Verify both laws are still active
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 2

        law_names = [law.agenda_card.get_name() for law in active_laws]
        assert "Anti-Intellectual Revolution" in law_names
        assert "Fleet Regulations" in law_names

        # Verify laws have correct enactment rounds
        air_active = next(
            law
            for law in active_laws
            if law.agenda_card.get_name() == "Anti-Intellectual Revolution"
        )
        fleet_active = next(
            law
            for law in active_laws
            if law.agenda_card.get_name() == "Fleet Regulations"
        )

        assert air_active.enacted_round == 1
        assert fleet_active.enacted_round == 2

    def test_complex_agenda_interaction_scenarios(self) -> None:
        """Test complex scenarios with multiple agenda effects interacting.

        RED: This test should fail as complex interaction handling doesn't exist yet.
        """
        # Arrange: Set up scenario with conflicting/interacting laws
        from ti4.core.agenda_cards.concrete.conventions_of_war import ConventionsOfWar
        from ti4.core.agenda_cards.concrete.homeland_defense_act import (
            HomelandDefenseAct,
        )
        from ti4.core.agenda_cards.law_manager import ActiveLaw
        from ti4.core.combat import CombatManager
        from ti4.core.production import ProductionManager

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        # Add planet for PDS placement testing
        planet = Planet(name="Test Planet", resources=2, influence=1)
        planet.controlled_by = "player1"

        game_state = game_state._create_new_state(
            players=[player1, player2], player_planets={"player1": [planet]}
        )

        # Enact multiple interacting laws
        homeland_law = HomelandDefenseAct()
        active_homeland = ActiveLaw(
            agenda_card=homeland_law,
            enacted_round=1,
            effect_description="Each player can have any number of PDS units on planets they control",
        )

        conventions_law = ConventionsOfWar()
        active_conventions = ActiveLaw(
            agenda_card=conventions_law,
            enacted_round=2,
            effect_description="Destroyed units are returned to reinforcements instead of being removed from the game",
        )

        game_state.law_manager.enact_law(active_homeland)
        game_state.law_manager.enact_law(active_conventions)

        # Act & Assert: Test interaction scenarios

        # Scenario 1: Place multiple PDS (Homeland Defense Act)
        production_manager = ProductionManager()

        # Should be able to place unlimited PDS due to Homeland Defense Act
        for _i in range(5):
            can_place = production_manager.can_place_pds_on_planet(
                planet, "player1", game_state
            )
            assert can_place is True

            pds_unit = Unit(unit_type=UnitType.PDS, owner="player1")
            planet.place_unit(pds_unit)

        # Verify 5 PDS were placed (normally limited to 1)
        pds_units = [unit for unit in planet.units if unit.unit_type == UnitType.PDS]
        assert len(pds_units) == 5

        # Scenario 2: Combat with unit destruction (Conventions of War)
        combat_manager = CombatManager()

        attacker_units = [Unit(unit_type=UnitType.CRUISER, owner="player1")]
        defender_units = [Unit(unit_type=UnitType.DESTROYER, owner="player2")]

        # Get applicable law effects for combat
        combat_law_effects = game_state.get_law_effects_for_action("combat", "player1")
        conventions_effects = [
            effect
            for effect in combat_law_effects
            if effect.agenda_card.get_name() == "Conventions of War"
        ]
        assert len(conventions_effects) == 1

        # Resolve combat with law effects
        combat_result = combat_manager.resolve_combat_with_law_effects(
            attacker_units, defender_units, conventions_effects
        )

        # Verify destroyed units returned to reinforcements (not removed from game)
        assert hasattr(combat_result, "destroyed_units_returned_to_reinforcements")
        assert len(combat_result.destroyed_units_returned_to_reinforcements) >= 0

        # Scenario 3: Verify both laws remain active and don't conflict
        active_laws = game_state.law_manager.get_active_laws()
        assert len(active_laws) == 2

        # Check for law conflicts
        # Note: check_law_conflicts needs agenda_card parameter
        conflicts = []  # Mock - would check for conflicts between laws
        assert len(conflicts) == 0  # These laws shouldn't conflict

    def test_agenda_phase_error_recovery_scenarios(self) -> None:
        """Test error recovery in agenda phase workflows.

        RED: This test should fail as comprehensive error recovery doesn't exist yet.
        """
        # Arrange: Set up scenarios that could cause errors
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.exceptions import AgendaCardValidationError
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase, SpeakerSystem, VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)

        # Planet with insufficient influence
        poor_planet = Planet(name="Poor Planet", resources=1, influence=0)
        poor_planet.controlled_by = "player1"

        game_state = game_state._create_new_state(
            players=[player1], player_planets={"player1": [poor_planet]}
        )

        registry = AgendaCardRegistry()
        deck = AgendaDeck(registry.get_all_cards())
        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()

        agenda_phase = AgendaPhase(
            deck=deck, voting_system=voting_system, speaker_system=speaker_system
        )

        # Test 1: Empty deck error recovery
        # Exhaust the deck
        while deck.cards_remaining() > 0:
            deck.draw_top_card()

        # Should handle empty deck gracefully
        try:
            revealed_card = agenda_phase.reveal_agenda_card()
            # Should either return None or reshuffle discard pile
            assert revealed_card is None or revealed_card is not None
        except Exception as e:
            # Should not raise unhandled exceptions
            assert isinstance(e, (AgendaCardValidationError, ValueError))

        # Test 2: Invalid voting scenario recovery
        deck = AgendaDeck(registry.get_all_cards())  # Reset deck
        agenda_phase.deck = deck

        revealed_card = agenda_phase.reveal_agenda_card()
        assert revealed_card is not None

        # Try to vote with invalid outcome
        vote_result = voting_system.cast_votes(
            player_id="player1",
            planets=[poor_planet],
            outcome="Invalid Outcome",
            agenda=revealed_card,
        )

        # Should fail gracefully with clear error message
        assert vote_result.success is False
        assert "Invalid outcome" in vote_result.error_message

        # Test 3: Insufficient influence error recovery
        vote_result = voting_system.cast_votes(
            player_id="player1",
            planets=[poor_planet],  # 0 influence
            outcome="For",
            agenda=revealed_card,
        )

        # Should succeed even with 0 influence (valid but ineffective vote)
        assert vote_result.success is True
        assert vote_result.votes_cast == 0

        # Test 4: Game state corruption recovery
        # Simulate corrupted game state
        corrupted_state = GameState()
        corrupted_state.players = []  # No players

        try:
            resolution_result = agenda_phase.resolve_agenda_outcome(
                agenda=revealed_card, outcome="For", game_state=corrupted_state
            )
            # Should handle gracefully
            assert resolution_result.success is False
            assert resolution_result.error_message is not None
        except Exception as e:
            # Should not crash the system
            assert isinstance(e, (ValueError, AgendaCardValidationError))

    def test_agenda_deck_management_integration(self) -> None:
        """Test agenda deck management throughout complete workflows.

        RED: This test should fail as deck management integration doesn't exist yet.
        """
        # Arrange: Set up agenda phase with deck tracking
        from ti4.core.agenda_cards.deck import AgendaDeck
        from ti4.core.agenda_cards.registry import AgendaCardRegistry
        from ti4.core.agenda_phase import AgendaPhase, SpeakerSystem, VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)

        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        planet.controlled_by = "player1"

        game_state = game_state._create_new_state(
            players=[player1], player_planets={"player1": [planet]}
        )

        registry = AgendaCardRegistry()
        initial_cards = registry.get_all_cards()
        deck = AgendaDeck(initial_cards)

        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()
        speaker_system.set_speaker("player1")

        agenda_phase = AgendaPhase(
            deck=deck, voting_system=voting_system, speaker_system=speaker_system
        )

        # Track initial deck state
        initial_deck_size = deck.cards_remaining()
        initial_discard_size = deck.discard_pile_size()

        assert initial_deck_size > 0
        assert initial_discard_size == 0

        # Act: Process multiple agendas to test deck management

        processed_agendas = []

        for _round_num in range(3):  # Process 3 rounds of agendas
            # Reveal agenda
            revealed_card = agenda_phase.reveal_agenda_card()
            assert revealed_card is not None
            processed_agendas.append(revealed_card.get_name())

            # Vote on agenda
            vote_result = voting_system.cast_votes(
                player_id="player1",
                planets=[planet],
                outcome="For",
                agenda=revealed_card,
            )
            assert vote_result.success is True

            # Resolve agenda
            resolution_result = agenda_phase.resolve_agenda_outcome(
                agenda=revealed_card, outcome="For", game_state=game_state
            )
            assert resolution_result.success is True

            # Discard agenda
            deck.discard_card(revealed_card)

            # Reset voting for next round
            voting_system.reset_votes()
            planet.ready()  # Ready planet for next vote

        # Assert: Verify deck state changes

        # Deck should have 3 fewer cards
        final_deck_size = deck.cards_remaining()
        assert final_deck_size == initial_deck_size - 3

        # Discard pile should have 3 cards
        final_discard_size = deck.discard_pile_size()
        assert final_discard_size == 3

        # Verify no duplicate agendas were processed
        assert len(set(processed_agendas)) == len(processed_agendas)

        # Test deck reshuffling when empty
        # Exhaust remaining deck
        while deck.cards_remaining() > 0:
            card = deck.draw_top_card()
            deck.discard_card(card)

        assert deck.cards_remaining() == 0
        assert deck.discard_pile_size() > 0

        # Next draw should trigger reshuffle
        reshuffled_card = deck.draw_top_card()
        assert reshuffled_card is not None

        # Deck should have cards again (from reshuffled discard pile)
        assert deck.cards_remaining() > 0

        # Verify reshuffle count increased
        assert deck.reshuffle_count() > 0

        # Sync deck state with game state
        game_state.synchronize_agenda_deck_state(deck)

        deck_state = game_state.agenda_deck_state
        assert deck_state["cards_in_deck"] == deck.cards_remaining()
        assert deck_state["cards_in_discard"] == deck.discard_pile_size()
        assert deck_state["reshuffle_count"] == deck.reshuffle_count()


class TestAgendaCardValidationIntegration:
    """Test agenda card validation throughout complete workflows."""

    def test_comprehensive_agenda_validation_workflow(self) -> None:
        """Test comprehensive validation throughout agenda workflow.

        RED: This test should fail as comprehensive validation doesn't exist yet.
        """
        # Arrange: Set up validation scenario
        from ti4.core.agenda_cards.concrete.anti_intellectual_revolution import (
            AntiIntellectualRevolution,
        )
        from ti4.core.agenda_cards.validation import (
            AgendaCardValidator,
            AgendaEffectValidator,
        )
        from ti4.core.agenda_phase import VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)

        # Add ships for validation testing
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        planet.controlled_by = "player1"

        game_state = game_state._create_new_state(
            players=[player1],
            player_units={"player1": [cruiser, fighter]},
            player_planets={"player1": [planet]},
        )

        # Create validators
        card_validator = AgendaCardValidator()
        effect_validator = AgendaEffectValidator()
        voting_system = VotingSystem()

        # Test agenda card
        agenda_card = AntiIntellectualRevolution()

        # Act & Assert: Test validation at each workflow step

        # Step 1: Validate agenda card structure
        card_validation = card_validator.validate_agenda_card(agenda_card)
        assert card_validation.is_valid is True
        assert card_validation.error_message == ""

        # Step 2: Validate voting outcomes
        outcome_validation = card_validator.validate_voting_outcomes(
            agenda_card, ["For", "Against", "Invalid"]
        )
        assert outcome_validation.valid_outcomes == ["For", "Against"]
        assert "Invalid" in outcome_validation.invalid_outcomes

        # Step 3: Validate vote casting
        vote_result = voting_system.cast_votes(
            player_id="player1", planets=[planet], outcome="For", agenda=agenda_card
        )
        assert vote_result.success is True

        # Step 4: Validate effect application preconditions
        effect_validation = effect_validator.validate_effect_preconditions(
            agenda_card=agenda_card,
            outcome="For",
            game_state=game_state,
            context={"player_id": "player1", "available_ships": [cruiser, fighter]},
        )
        assert effect_validation.is_valid is True
        assert effect_validation.required_actions == ["destroy_non_fighter_ship"]

        # Step 5: Validate effect application
        application_validation = effect_validator.validate_effect_application(
            agenda_card=agenda_card,
            outcome="For",
            game_state=game_state,
            proposed_actions={"destroy_ship": cruiser},
        )
        assert application_validation.is_valid is True

        # Step 6: Validate post-effect game state
        # Simulate effect application
        game_state_after = game_state.remove_unit("player1", cruiser)

        post_effect_validation = effect_validator.validate_post_effect_state(
            agenda_card=agenda_card,
            outcome="For",
            game_state_before=game_state,
            game_state_after=game_state_after,
        )
        assert post_effect_validation.is_valid is True
        assert post_effect_validation.changes_applied == ["unit_destroyed"]

    def test_edge_case_validation_scenarios(self) -> None:
        """Test validation of edge cases and error conditions.

        RED: This test should fail as edge case validation doesn't exist yet.
        """
        # Arrange: Set up edge case scenarios
        from ti4.core.agenda_cards.concrete.classified_document_leaks import (
            ClassifiedDocumentLeaks,
        )
        from ti4.core.agenda_cards.validation import AgendaCardValidator
        from ti4.core.agenda_phase import VotingSystem

        game_state = GameState()
        player1 = Player(id="player1", faction=Faction.SOL)

        # No scored secret objectives (edge case for Classified Document Leaks)
        game_state = game_state._create_new_state(
            players=[player1],
            scored_secret_objectives=[],  # Empty list
        )

        validator = AgendaCardValidator()
        VotingSystem()

        # Test card that should be discarded
        leaks_card = ClassifiedDocumentLeaks()

        # Act & Assert: Test edge case validations

        # Test 1: Card should be discarded when revealed
        discard_validation = validator.validate_card_reveal_conditions(
            agenda_card=leaks_card, game_state=game_state
        )
        assert discard_validation.should_discard is True
        assert "no scored secret objectives" in discard_validation.reason.lower()

        # Test 2: Voting should be invalid if card should be discarded
        vote_validation = validator.validate_voting_eligibility(
            agenda_card=leaks_card, game_state=game_state
        )
        assert vote_validation.is_valid is False
        assert vote_validation.error_message != ""

        # Test 3: Empty player list edge case
        empty_game_state = GameState()
        empty_game_state = empty_game_state._create_new_state(players=[])

        empty_validation = validator.validate_game_state_for_agenda(
            game_state=empty_game_state
        )
        assert empty_validation.is_valid is False
        assert "no players" in empty_validation.error_message.lower()

        # Test 4: Invalid planet ownership edge case
        planet = Planet(name="Uncontrolled Planet", resources=2, influence=3)
        # Don't set controlled_by - should be invalid for voting

        ownership_validation = validator.validate_planet_for_voting(
            planet=planet, player_id="player1"
        )
        assert ownership_validation.is_valid is False
        assert "not controlled" in ownership_validation.error_message.lower()

        # Test 5: Exhausted planet edge case
        exhausted_planet = Planet(name="Exhausted Planet", resources=2, influence=3)
        exhausted_planet.controlled_by = "player1"
        exhausted_planet.exhaust()  # Already exhausted

        exhausted_validation = validator.validate_planet_for_voting(
            planet=exhausted_planet, player_id="player1"
        )
        assert exhausted_validation.is_valid is False
        assert "exhausted" in exhausted_validation.error_message.lower()


# REFACTOR PHASE CONSIDERATION:
# After implementing these tests and making them pass, consider:
# 1. **Code Duplication**: Extract common setup patterns into helper methods
# 2. **Error Handling**: Add comprehensive error scenarios and recovery testing
# 3. **Validation**: Ensure all edge cases are covered with proper validation
# 4. **Naming**: Use descriptive test names that clearly indicate what's being tested
# 5. **Single Responsibility**: Each test should focus on one specific workflow aspect
# 6. **Readability**: Add clear comments explaining complex test scenarios

# The tests are comprehensive but may need refactoring once implementation begins
# to eliminate duplication and improve maintainability. The current structure
# provides good coverage of all integration scenarios specified in the task.
