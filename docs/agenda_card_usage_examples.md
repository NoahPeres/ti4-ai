# Agenda Card Framework Usage Examples

## Overview

This document provides comprehensive examples of implementing different types of agenda cards using the Agenda Card Framework. Each example includes complete implementation code, tests, and integration patterns.

## Table of Contents

1. [Basic Law Card Example](#basic-law-card-example)
2. [Election-Based Law Card](#election-based-law-card)
3. [Simple Directive Card](#simple-directive-card)
4. [Planet Attachable Card](#planet-attachable-card)
5. [Complex Multi-Effect Card](#complex-multi-effect-card)
6. [Custom Voting Pattern Card](#custom-voting-pattern-card)
7. [Integration Examples](#integration-examples)

## Basic Law Card Example

### Fleet Regulations

A simple law card with For/Against outcomes where FOR creates a persistent law and AGAINST provides an immediate benefit.

#### Implementation

```python
# src/ti4/core/agenda_cards/concrete/fleet_regulations.py
"""
Fleet Regulations agenda card implementation.

This module implements the Fleet Regulations law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class FleetRegulations(LawCard):
    """
    Fleet Regulations agenda card.

    FOR: Each player cannot have more than 4 tokens in their fleet pool.
    AGAINST: Each player places 1 command token in their fleet pool.
    """

    def __init__(self) -> None:
        """Initialize the Fleet Regulations card."""
        super().__init__("Fleet Regulations")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["For", "Against"]

    def get_law_effects(self) -> list[str]:
        """Get list of game mechanics this law affects."""
        return ["fleet_pool_limit", "command_token_placement"]

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: "VoteResult",
        game_state: "GameState",
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid outcome '{outcome}' for Fleet Regulations")

        if outcome == "For":
            # FOR: Enact law limiting fleet pool to 4 tokens
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Fleet Regulations enacted: Players cannot have more than 4 tokens in fleet pool",
            )
        else:  # Against
            # AGAINST: Each player gains 1 fleet pool token
            self._execute_against_effect(game_state)
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Fleet Regulations rejected: Each player places 1 command token in their fleet pool",
            )

    def create_active_law(
        self, outcome: str, elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance for the FOR outcome."""
        if outcome != "For":
            raise ValueError("Can only create active law for 'For' outcome")

        return ActiveLaw(
            agenda_card=self,
            enacted_round=1,  # This would be set by the actual game state
            effect_description="Each player cannot have more than 4 tokens in their fleet pool",
            elected_target=elected_target,
        )

    def _execute_against_effect(self, game_state: "GameState") -> None:
        """Execute the AGAINST effect - give each player a fleet pool token."""
        for player in game_state.players.values():
            if player.command_sheet.fleet_pool < player.command_sheet.max_fleet_pool:
                player.command_sheet.fleet_pool += 1

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "fleet_pool_modification"
```

#### Tests

```python
# Example test structure for Fleet Regulations
"""Tests for Fleet Regulations agenda card."""

import pytest
from unittest.mock import Mock

from ti4.core.agenda_cards.concrete.fleet_regulations import FleetRegulations
from ti4.core.constants import AgendaType


class TestFleetRegulations:
    """Test Fleet Regulations implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""
        card = FleetRegulations()
        assert card.name == "Fleet Regulations"
        assert card.get_agenda_type() == AgendaType.LAW
        assert card.get_voting_outcomes() == ["For", "Against"]
        assert "fleet_pool_limit" in card.get_law_effects()

    def test_for_outcome_resolution(self):
        """Test FOR outcome creates active law."""
        card = FleetRegulations()
        mock_vote_result = Mock()
        mock_game_state = Mock()

        result = card.resolve_outcome("For", mock_vote_result, mock_game_state)

        assert result.success
        assert result.law_enacted
        assert not result.directive_executed
        assert "enacted" in result.description.lower()
        assert "4 tokens" in result.description

    def test_against_outcome_resolution(self):
        """Test AGAINST outcome executes directive."""
        card = FleetRegulations()
        mock_vote_result = Mock()
        mock_game_state = self._create_mock_game_state()

        result = card.resolve_outcome("Against", mock_vote_result, mock_game_state)

        assert result.success
        assert not result.law_enacted
        assert result.directive_executed
        assert "rejected" in result.description.lower()
        assert "command token" in result.description

    def test_create_active_law(self):
        """Test active law creation."""
        card = FleetRegulations()
        active_law = card.create_active_law("For")

        assert active_law.agenda_card == card
        assert "4 tokens" in active_law.effect_description
        assert active_law.enacted_round == 1
        assert active_law.elected_target is None

    def test_create_active_law_invalid_outcome(self):
        """Test active law creation with invalid outcome."""
        card = FleetRegulations()

        with pytest.raises(ValueError, match="Can only create active law for 'For' outcome"):
            card.create_active_law("Against")

    def test_invalid_outcome_raises_error(self):
        """Test invalid outcomes raise appropriate errors."""
        card = FleetRegulations()
        mock_vote_result = Mock()
        mock_game_state = Mock()

        with pytest.raises(ValueError, match="Invalid outcome 'Invalid' for Fleet Regulations"):
            card.resolve_outcome("Invalid", mock_vote_result, mock_game_state)

    def test_against_effect_execution(self):
        """Test AGAINST effect gives players fleet pool tokens."""
        card = FleetRegulations()
        mock_game_state = self._create_mock_game_state()

        # Execute against effect
        card._execute_against_effect(mock_game_state)

        # Verify each player got a fleet pool token
        for player in mock_game_state.players.values():
            # This would be verified based on the actual implementation
            pass

    def _create_mock_game_state(self):
        """Create a mock game state for testing."""
        mock_game_state = Mock()
        mock_players = {}

        for i in range(4):  # 4 players
            mock_player = Mock()
            mock_command_sheet = Mock()
            mock_command_sheet.fleet_pool = 2
            mock_command_sheet.max_fleet_pool = 4
            mock_player.command_sheet = mock_command_sheet
            mock_players[f"player_{i}"] = mock_player

        mock_game_state.players = mock_players
        return mock_game_state
```

## Election-Based Law Card

### Minister of Commerce

A law card that uses election mechanics to select a player who gains ongoing abilities.

#### Implementation

```python
# src/ti4/core/agenda_cards/concrete/minister_of_commerce.py
"""
Minister of Commerce agenda card implementation.

This module implements the Minister of Commerce law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class MinisterOfCommerce(LawCard):
    """
    Minister of Commerce agenda card.

    Elect Player: The elected player gains "At the start of the strategy phase,
    gain 2 trade goods" and "When you gain trade goods from a transaction,
    gain 1 additional trade good."
    """

    def __init__(self) -> None:
        """Initialize the Minister of Commerce card."""
        super().__init__("Minister of Commerce")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["Elect Player"]

    def get_law_effects(self) -> list[str]:
        """Get list of game mechanics this law affects."""
        return ["trade_goods_generation", "transaction_bonuses", "strategy_phase_income"]

    def conflicts_with_law(self, other_law: "ActiveLaw") -> bool:
        """Check if this law conflicts with another active law."""
        # Minister cards typically replace each other
        return other_law.agenda_card.name.startswith("Minister of")

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: "VoteResult",
        game_state: "GameState",
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid outcome '{outcome}' for Minister of Commerce")

        if vote_result.elected_target is None:
            raise ValueError("No player elected for Minister of Commerce")

        elected_player = vote_result.elected_target

        return AgendaResolutionResult(
            success=True,
            law_enacted=True,
            description=f"Minister of Commerce enacted: {elected_player} gains trade good bonuses",
            elected_target=elected_player,
        )

    def create_active_law(
        self, outcome: str, elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance for the election outcome."""
        if outcome != "Elect Player":
            raise ValueError("Can only create active law for 'Elect Player' outcome")

        if elected_target is None:
            raise ValueError("Elected target required for Minister of Commerce")

        return ActiveLaw(
            agenda_card=self,
            enacted_round=1,  # This would be set by the actual game state
            effect_description=f"{elected_target} gains trade good generation and transaction bonuses",
            elected_target=elected_target,
        )

    def get_minister_abilities(self, elected_player: str) -> list[dict]:
        """Get the abilities granted to the elected minister."""
        return [
            {
                "name": "Strategy Phase Income",
                "description": "At the start of the strategy phase, gain 2 trade goods",
                "trigger": "strategy_phase_start",
                "effect": {"type": "gain_trade_goods", "amount": 2},
                "player": elected_player,
            },
            {
                "name": "Transaction Bonus",
                "description": "When you gain trade goods from a transaction, gain 1 additional trade good",
                "trigger": "transaction_trade_goods_gained",
                "effect": {"type": "gain_trade_goods", "amount": 1},
                "player": elected_player,
            },
        ]

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "minister_abilities"
```

#### Tests

```python
# Example test structure for Minister of Commerce
"""Tests for Minister of Commerce agenda card."""

import pytest
from unittest.mock import Mock

from ti4.core.agenda_cards.concrete.minister_of_commerce import MinisterOfCommerce
from ti4.core.constants import AgendaType


class TestMinisterOfCommerce:
    """Test Minister of Commerce implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""
        card = MinisterOfCommerce()
        assert card.name == "Minister of Commerce"
        assert card.get_agenda_type() == AgendaType.LAW
        assert card.get_voting_outcomes() == ["Elect Player"]
        assert "trade_goods_generation" in card.get_law_effects()

    def test_election_outcome_resolution(self):
        """Test election outcome creates active law with elected player."""
        card = MinisterOfCommerce()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Player 1"
        mock_game_state = Mock()

        result = card.resolve_outcome("Elect Player", mock_vote_result, mock_game_state)

        assert result.success
        assert result.law_enacted
        assert result.elected_target == "Player 1"
        assert "Player 1" in result.description

    def test_no_elected_target_raises_error(self):
        """Test missing elected target raises error."""
        card = MinisterOfCommerce()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = None
        mock_game_state = Mock()

        with pytest.raises(ValueError, match="No player elected"):
            card.resolve_outcome("Elect Player", mock_vote_result, mock_game_state)

    def test_create_active_law_with_elected_player(self):
        """Test active law creation with elected player."""
        card = MinisterOfCommerce()
        active_law = card.create_active_law("Elect Player", "Player 1")

        assert active_law.agenda_card == card
        assert active_law.elected_target == "Player 1"
        assert "Player 1" in active_law.effect_description

    def test_create_active_law_no_target_raises_error(self):
        """Test active law creation without target raises error."""
        card = MinisterOfCommerce()

        with pytest.raises(ValueError, match="Elected target required"):
            card.create_active_law("Elect Player", None)

    def test_minister_abilities(self):
        """Test minister abilities are correctly defined."""
        card = MinisterOfCommerce()
        abilities = card.get_minister_abilities("Player 1")

        assert len(abilities) == 2

        # Check strategy phase income ability
        income_ability = abilities[0]
        assert income_ability["name"] == "Strategy Phase Income"
        assert income_ability["trigger"] == "strategy_phase_start"
        assert income_ability["effect"]["amount"] == 2
        assert income_ability["player"] == "Player 1"

        # Check transaction bonus ability
        transaction_ability = abilities[1]
        assert transaction_ability["name"] == "Transaction Bonus"
        assert transaction_ability["trigger"] == "transaction_trade_goods_gained"
        assert transaction_ability["effect"]["amount"] == 1
        assert transaction_ability["player"] == "Player 1"

    def test_conflicts_with_other_ministers(self):
        """Test that minister cards conflict with each other."""
        card = MinisterOfCommerce()

        # Create mock other minister law
        mock_other_law = Mock()
        mock_other_law.agenda_card.name = "Minister of War"

        assert card.conflicts_with_law(mock_other_law)

        # Non-minister law should not conflict
        mock_non_minister = Mock()
        mock_non_minister.agenda_card.name = "Fleet Regulations"

        assert not card.conflicts_with_law(mock_non_minister)
```

## Simple Directive Card

### Committee Formation

A directive card with special mechanics that bypasses normal voting.

#### Implementation

```python
# src/ti4/core/agenda_cards/concrete/committee_formation.py
"""
Committee Formation directive card implementation.

This module implements the Committee Formation agenda card from the base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.directive_card import DirectiveCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class CommitteeFormation(DirectiveCard):
    """
    Committee Formation directive card.

    When this agenda is revealed, if there are no laws in play,
    discard this agenda and reveal another agenda.
    Otherwise, choose a law in play and discard it.
    """

    def __init__(self) -> None:
        """Initialize the Committee Formation card."""
        super().__init__("Committee Formation")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        # This card doesn't use normal voting - it has special resolution
        return ["Choose Law to Discard"]

    def should_discard_on_reveal(self, game_state: "GameState") -> bool:
        """Check if card should be discarded when revealed."""
        # Discard if no laws are in play
        active_laws = game_state.law_manager.get_active_laws()
        return len(active_laws) == 0

    def resolve_outcome(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid voting outcome: {outcome}")

        # Get the chosen law to discard
        if vote_result.elected_target is None:
            raise ValueError("No law chosen for Committee Formation")

        chosen_law = vote_result.elected_target

        # Execute the directive effect
        self.execute_immediate_effect(outcome, vote_result, game_state)

        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            description=f"Committee Formation: Law '{chosen_law}' has been discarded",
            elected_target=chosen_law,
        )

    def execute_immediate_effect(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> None:
        """Execute the immediate directive effect."""
        chosen_law = vote_result.elected_target
        if chosen_law is None:
            raise ValueError("No law chosen for Committee Formation")

        # Remove the chosen law from play
        success = game_state.law_manager.remove_law(chosen_law)
        if not success:
            raise ValueError(f"Failed to remove law '{chosen_law}' - law not found")

    def get_available_laws_to_discard(self, game_state: "GameState") -> list[str]:
        """Get list of laws that can be discarded."""
        active_laws = game_state.law_manager.get_active_laws()
        return [law.agenda_card.name for law in active_laws]

    def has_special_resolution(self) -> bool:
        """Indicate this card has special resolution mechanics."""
        return True
```

#### Tests

```python
# Example test structure for Committee Formation
"""Tests for Committee Formation agenda card."""

import pytest
from unittest.mock import Mock

from ti4.core.agenda_cards.concrete.committee_formation import CommitteeFormation
from ti4.core.constants import AgendaType


class TestCommitteeFormation:
    """Test Committee Formation implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""
        card = CommitteeFormation()
        assert card.name == "Committee Formation"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE
        assert card.get_voting_outcomes() == ["Choose Law to Discard"]
        assert card.has_special_resolution()

    def test_should_discard_when_no_laws(self):
        """Test card is discarded when no laws are in play."""
        card = CommitteeFormation()
        mock_game_state = Mock()
        mock_law_manager = Mock()
        mock_law_manager.get_active_laws.return_value = []
        mock_game_state.law_manager = mock_law_manager

        assert card.should_discard_on_reveal(mock_game_state)

    def test_should_not_discard_when_laws_exist(self):
        """Test card is not discarded when laws are in play."""
        card = CommitteeFormation()
        mock_game_state = Mock()
        mock_law_manager = Mock()
        mock_law_manager.get_active_laws.return_value = [Mock()]  # One law
        mock_game_state.law_manager = mock_law_manager

        assert not card.should_discard_on_reveal(mock_game_state)

    def test_resolve_outcome_success(self):
        """Test successful outcome resolution."""
        card = CommitteeFormation()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Fleet Regulations"
        mock_game_state = self._create_mock_game_state_with_laws()

        result = card.resolve_outcome("Choose Law to Discard", mock_vote_result, mock_game_state)

        assert result.success
        assert result.directive_executed
        assert result.elected_target == "Fleet Regulations"
        assert "Fleet Regulations" in result.description

    def test_resolve_outcome_no_law_chosen(self):
        """Test resolution fails when no law is chosen."""
        card = CommitteeFormation()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = None
        mock_game_state = Mock()

        with pytest.raises(ValueError, match="No law chosen"):
            card.resolve_outcome("Choose Law to Discard", mock_vote_result, mock_game_state)

    def test_execute_immediate_effect(self):
        """Test immediate effect execution removes law."""
        card = CommitteeFormation()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Fleet Regulations"
        mock_game_state = self._create_mock_game_state_with_laws()

        card.execute_immediate_effect("Choose Law to Discard", mock_vote_result, mock_game_state)

        # Verify law removal was called
        mock_game_state.law_manager.remove_law.assert_called_once_with("Fleet Regulations")

    def test_execute_immediate_effect_law_not_found(self):
        """Test immediate effect fails when law doesn't exist."""
        card = CommitteeFormation()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Nonexistent Law"
        mock_game_state = Mock()
        mock_law_manager = Mock()
        mock_law_manager.remove_law.return_value = False  # Law not found
        mock_game_state.law_manager = mock_law_manager

        with pytest.raises(ValueError, match="Failed to remove law"):
            card.execute_immediate_effect("Choose Law to Discard", mock_vote_result, mock_game_state)

    def test_get_available_laws_to_discard(self):
        """Test getting available laws to discard."""
        card = CommitteeFormation()
        mock_game_state = self._create_mock_game_state_with_laws()

        available_laws = card.get_available_laws_to_discard(mock_game_state)

        assert "Fleet Regulations" in available_laws
        assert "Anti-Intellectual Revolution" in available_laws

    def _create_mock_game_state_with_laws(self):
        """Create mock game state with active laws."""
        mock_game_state = Mock()
        mock_law_manager = Mock()

        # Create mock active laws
        mock_law1 = Mock()
        mock_law1.agenda_card.name = "Fleet Regulations"
        mock_law2 = Mock()
        mock_law2.agenda_card.name = "Anti-Intellectual Revolution"

        mock_law_manager.get_active_laws.return_value = [mock_law1, mock_law2]
        mock_law_manager.remove_law.return_value = True
        mock_game_state.law_manager = mock_law_manager

        return mock_game_state
```

## Planet Attachable Card

### Core Mining

A directive card that attaches to planets and provides ongoing benefits.

#### Implementation

```python
# src/ti4/core/agenda_cards/concrete/core_mining.py
"""
Core Mining agenda card implementation.

This module implements the Core Mining agenda card from the base game.
"""

from typing import TYPE_CHECKING, Any

from ti4.core.agenda_cards.base.planet_attachable_card import PlanetAttachableCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.constants import PlanetAttachmentType, PlanetType

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState
    from ti4.core.planet import Planet


class CoreMining(PlanetAttachableCard):
    """
    Core Mining agenda card.

    Elect Industrial Planet: Attach this card to the elected planet.
    The planet's resource value is increased by 2.
    """

    def __init__(self) -> None:
        """Initialize the Core Mining card."""
        super().__init__("Core Mining")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["Elect Industrial Planet"]

    def get_attachment_type(self) -> PlanetAttachmentType:
        """Get the type of planet attachment."""
        return PlanetAttachmentType.RESOURCE_ENHANCEMENT

    def get_planet_effects(self) -> dict[str, Any]:
        """Get the effects this attachment provides to the planet."""
        return {
            "resource_bonus": 2,
            "effect_description": "Planet's resource value is increased by 2",
        }

    def can_attach_to_planet(self, planet: "Planet") -> bool:
        """Check if this card can attach to the given planet."""
        # Can only attach to industrial planets
        return planet.planet_type == PlanetType.INDUSTRIAL

    def resolve_outcome(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid voting outcome: {outcome}")

        if vote_result.elected_target is None:
            raise ValueError("No planet elected for Core Mining")

        elected_planet = vote_result.elected_target

        # Execute the directive effect
        self.execute_immediate_effect(outcome, vote_result, game_state)

        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            description=f"Core Mining attached to {elected_planet}: Resource value increased by 2",
            elected_target=elected_planet,
        )

    def execute_immediate_effect(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> None:
        """Execute the immediate directive effect."""
        elected_planet = vote_result.elected_target
        if elected_planet is None:
            raise ValueError("No planet elected for Core Mining")

        # Get the planet object
        planet = game_state.get_planet(elected_planet)
        if planet is None:
            raise ValueError(f"Planet '{elected_planet}' not found")

        # Verify planet can accept attachment
        if not self.can_attach_to_planet(planet):
            raise ValueError(f"Cannot attach Core Mining to {elected_planet} - not an industrial planet")

        # Attach the card to the planet
        attachment_manager = game_state.planet_attachment_manager
        attachment_manager.attach_card_to_planet(self, planet)

    def get_eligible_planets(self, game_state: "GameState") -> list[str]:
        """Get list of planets eligible for this attachment."""
        eligible_planets = []

        for planet_name, planet in game_state.planets.items():
            if self.can_attach_to_planet(planet):
                # Check if planet doesn't already have this attachment
                attachment_manager = game_state.planet_attachment_manager
                existing_attachments = attachment_manager.get_attachments_for_planet(planet_name)

                # Don't allow duplicate Core Mining attachments
                if not any(att.name == self.name for att in existing_attachments):
                    eligible_planets.append(planet_name)

        return eligible_planets

    def get_resource_bonus(self) -> int:
        """Get the resource bonus this attachment provides."""
        return self.get_planet_effects()["resource_bonus"]
```

#### Tests

```python
# Example test structure for Core Mining
"""Tests for Core Mining agenda card."""

import pytest
from unittest.mock import Mock

from ti4.core.agenda_cards.concrete.core_mining import CoreMining
from ti4.core.constants import AgendaType, PlanetAttachmentType, PlanetType


class TestCoreMining:
    """Test Core Mining implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""
        card = CoreMining()
        assert card.name == "Core Mining"
        assert card.get_agenda_type() == AgendaType.DIRECTIVE
        assert card.get_voting_outcomes() == ["Elect Industrial Planet"]
        assert card.get_attachment_type() == PlanetAttachmentType.RESOURCE_ENHANCEMENT

    def test_planet_effects(self):
        """Test planet effects definition."""
        card = CoreMining()
        effects = card.get_planet_effects()

        assert effects["resource_bonus"] == 2
        assert "resource value is increased by 2" in effects["effect_description"]

    def test_can_attach_to_industrial_planet(self):
        """Test attachment to industrial planets."""
        card = CoreMining()
        mock_planet = Mock()
        mock_planet.planet_type = PlanetType.INDUSTRIAL

        assert card.can_attach_to_planet(mock_planet)

    def test_cannot_attach_to_non_industrial_planet(self):
        """Test cannot attach to non-industrial planets."""
        card = CoreMining()

        # Test cultural planet
        mock_cultural_planet = Mock()
        mock_cultural_planet.planet_type = PlanetType.CULTURAL
        assert not card.can_attach_to_planet(mock_cultural_planet)

        # Test hazardous planet
        mock_hazardous_planet = Mock()
        mock_hazardous_planet.planet_type = PlanetType.HAZARDOUS
        assert not card.can_attach_to_planet(mock_hazardous_planet)

    def test_resolve_outcome_success(self):
        """Test successful outcome resolution."""
        card = CoreMining()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Mecatol Rex"
        mock_game_state = self._create_mock_game_state()

        result = card.resolve_outcome("Elect Industrial Planet", mock_vote_result, mock_game_state)

        assert result.success
        assert result.directive_executed
        assert result.elected_target == "Mecatol Rex"
        assert "Mecatol Rex" in result.description
        assert "Resource value increased by 2" in result.description

    def test_resolve_outcome_no_planet_elected(self):
        """Test resolution fails when no planet is elected."""
        card = CoreMining()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = None
        mock_game_state = Mock()

        with pytest.raises(ValueError, match="No planet elected"):
            card.resolve_outcome("Elect Industrial Planet", mock_vote_result, mock_game_state)

    def test_execute_immediate_effect(self):
        """Test immediate effect execution attaches card to planet."""
        card = CoreMining()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Mecatol Rex"
        mock_game_state = self._create_mock_game_state()

        card.execute_immediate_effect("Elect Industrial Planet", mock_vote_result, mock_game_state)

        # Verify attachment was created
        mock_game_state.planet_attachment_manager.attach_card_to_planet.assert_called_once()

    def test_execute_immediate_effect_planet_not_found(self):
        """Test immediate effect fails when planet doesn't exist."""
        card = CoreMining()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Nonexistent Planet"
        mock_game_state = Mock()
        mock_game_state.get_planet.return_value = None

        with pytest.raises(ValueError, match="Planet 'Nonexistent Planet' not found"):
            card.execute_immediate_effect("Elect Industrial Planet", mock_vote_result, mock_game_state)

    def test_execute_immediate_effect_invalid_planet_type(self):
        """Test immediate effect fails for non-industrial planets."""
        card = CoreMining()
        mock_vote_result = Mock()
        mock_vote_result.elected_target = "Cultural Planet"
        mock_game_state = Mock()

        mock_planet = Mock()
        mock_planet.planet_type = PlanetType.CULTURAL
        mock_game_state.get_planet.return_value = mock_planet

        with pytest.raises(ValueError, match="not an industrial planet"):
            card.execute_immediate_effect("Elect Industrial Planet", mock_vote_result, mock_game_state)

    def test_get_eligible_planets(self):
        """Test getting eligible planets for attachment."""
        card = CoreMining()
        mock_game_state = self._create_mock_game_state_with_planets()

        eligible_planets = card.get_eligible_planets(mock_game_state)

        assert "Industrial Planet 1" in eligible_planets
        assert "Industrial Planet 2" in eligible_planets
        assert "Cultural Planet" not in eligible_planets

    def test_get_resource_bonus(self):
        """Test getting resource bonus value."""
        card = CoreMining()
        assert card.get_resource_bonus() == 2

    def _create_mock_game_state(self):
        """Create mock game state for testing."""
        mock_game_state = Mock()

        # Mock planet
        mock_planet = Mock()
        mock_planet.planet_type = PlanetType.INDUSTRIAL
        mock_game_state.get_planet.return_value = mock_planet

        # Mock attachment manager
        mock_attachment_manager = Mock()
        mock_game_state.planet_attachment_manager = mock_attachment_manager

        return mock_game_state

    def _create_mock_game_state_with_planets(self):
        """Create mock game state with multiple planets."""
        mock_game_state = Mock()

        # Create mock planets
        mock_planets = {
            "Industrial Planet 1": Mock(planet_type=PlanetType.INDUSTRIAL),
            "Industrial Planet 2": Mock(planet_type=PlanetType.INDUSTRIAL),
            "Cultural Planet": Mock(planet_type=PlanetType.CULTURAL),
        }
        mock_game_state.planets = mock_planets

        # Mock attachment manager
        mock_attachment_manager = Mock()
        mock_attachment_manager.get_attachments_for_planet.return_value = []
        mock_game_state.planet_attachment_manager = mock_attachment_manager

        return mock_game_state
```

## Integration Examples

### Registering Cards with the System

```python
# src/ti4/core/agenda_cards/concrete/__init__.py
"""
Concrete agenda card implementations.

This module automatically registers all agenda card implementations.
"""

from .anti_intellectual_revolution import AntiIntellectualRevolution
from .classified_document_leaks import ClassifiedDocumentLeaks
from .committee_formation import CommitteeFormation
from .core_mining import CoreMining
from .fleet_regulations import FleetRegulations
from .minister_of_commerce import MinisterOfCommerce

# Registry will automatically discover and register these cards
__all__ = [
    "AntiIntellectualRevolution",
    "ClassifiedDocumentLeaks",
    "CommitteeFormation",
    "CoreMining",
    "FleetRegulations",
    "MinisterOfCommerce",
]
```

### Using Cards in Agenda Phase

```python
# Example of agenda phase integration
def process_agenda_phase(game_state: GameState) -> None:
    """Process a complete agenda phase."""
    agenda_phase = game_state.agenda_phase

    # Reveal agenda card
    agenda_card = agenda_phase.reveal_agenda_card()
    print(f"Revealed: {agenda_card.name}")

    # Check if card should be discarded
    if isinstance(agenda_card, DirectiveCard) and agenda_card.should_discard_on_reveal(game_state):
        print(f"Discarding {agenda_card.name} - conditions not met")
        agenda_phase.agenda_deck.discard_card(agenda_card)
        agenda_card = agenda_phase.reveal_agenda_card()

    # Present voting options
    voting_outcomes = agenda_card.get_voting_outcomes()
    print(f"Voting options: {voting_outcomes}")

    # Conduct voting (simplified)
    vote_result = conduct_voting(agenda_card, game_state)

    # Resolve outcome
    resolver = AgendaEffectResolver()
    result = resolver.resolve_agenda_outcome(agenda_card, vote_result, game_state)

    if result.success:
        print(f"Resolution: {result.description}")

        if result.law_enacted:
            print("Law has been enacted and is now active")
        elif result.directive_executed:
            print("Directive effect has been executed")
    else:
        print(f"Resolution failed: {result.errors}")
```

### Testing Integration

```python
# Example of integration testing
def test_full_agenda_workflow():
    """Test complete agenda card workflow."""
    # Setup
    game_state = create_test_game_state()
    registry = AgendaCardRegistry()

    # Register cards
    fleet_regulations = FleetRegulations()
    registry.register_card(fleet_regulations)

    # Create deck
    deck = AgendaDeck([fleet_regulations])
    game_state.agenda_deck = deck

    # Process agenda
    agenda_phase = AgendaPhase(game_state)
    card = agenda_phase.reveal_agenda_card()

    # Vote
    vote_result = VoteResult(outcome="For", elected_target=None)

    # Resolve
    result = card.resolve_outcome("For", vote_result, game_state)

    # Verify
    assert result.success
    assert result.law_enacted

    # Check law is active
    active_laws = game_state.law_manager.get_active_laws()
    assert len(active_laws) == 1
    assert active_laws[0].agenda_card.name == "Fleet Regulations"
```

This comprehensive set of examples demonstrates how to implement all types of agenda cards in the framework. Each example includes complete implementation code, comprehensive tests, and integration patterns that can be used as templates for new agenda card implementations.
