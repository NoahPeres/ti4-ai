"""Rule 35: EXPLORATION

This module implements the exploration system for Twilight Imperium 4th Edition.

LRR 35: Planets and some space areas can be explored, yielding varying results
determined by the cards drawn from the exploration decks.
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ti4.core.abilities import Ability
from ti4.core.card_types import ExplorationCardProtocol, PlanetTrait
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player


class ExplorationCardType(Enum):
    """Types of exploration cards."""

    NORMAL = "normal"
    ATTACHMENT = "attachment"
    RELIC_FRAGMENT = "relic_fragment"


@dataclass
class ExplorationCard(ExplorationCardProtocol):
    """Represents an exploration card.

    LRR 35.7: Exploration cards have different types that affect resolution.
    """

    name: str
    trait: PlanetTrait
    card_type: ExplorationCardType
    effect: str
    ability: Ability | None = None

    @property
    def is_attachment(self) -> bool:
        """Check if this is an attachment card (Rule 35.8)."""
        return self.card_type == ExplorationCardType.ATTACHMENT

    @property
    def is_relic_fragment(self) -> bool:
        """Check if this is a relic fragment card (Rule 35.9)."""
        return self.card_type == ExplorationCardType.RELIC_FRAGMENT

    @property
    def should_be_discarded(self) -> bool:
        """Check if this card should be discarded after resolution (Rule 35.7)."""
        return not (self.is_attachment or self.is_relic_fragment)


@dataclass
class ExplorationResult:
    """Result of an exploration action."""

    success: bool = False
    exploration_triggered: bool = False
    deck_used: PlanetTrait | None = None
    card_drawn: ExplorationCard | None = None
    card_discarded: bool = False
    card_attached: bool = False
    relic_fragment_gained: bool = False
    relic_drawn: bool = False
    frontier_token_removed: bool = False
    effect_applied: bool = False
    planet_name: str | None = None


class ExplorationDeck:
    """Manages an exploration deck and its discard pile.

    LRR 35.7a: When deck is empty, discard pile is shuffled to form new deck.
    """

    def __init__(self, trait: PlanetTrait):
        self.trait = trait
        self.cards: list[ExplorationCard] = []
        self.discard_pile: list[ExplorationCard] = []
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        """Initialize deck with sample cards for testing.

        Note: In a full implementation, this would load from game data files.
        """
        deck_configs = {
            PlanetTrait.CULTURAL: [
                (
                    "Ancient Burial Sites",
                    ExplorationCardType.ATTACHMENT,
                    "This planet provides +1 influence",
                ),
                (
                    "Cultural Research",
                    ExplorationCardType.NORMAL,
                    "Gain 2 influence",
                ),
                (
                    "Relic Fragment",
                    ExplorationCardType.RELIC_FRAGMENT,
                    "Purge this card to draw 1 relic",
                ),
            ],
            PlanetTrait.HAZARDOUS: [
                (
                    "Volatile Fuel Source",
                    ExplorationCardType.ATTACHMENT,
                    "This planet provides +1 resource",
                ),
                (
                    "Dangerous Wildlife",
                    ExplorationCardType.NORMAL,
                    "Lose 1 infantry or gain 1 trade good",
                ),
                (
                    "Relic Fragment",
                    ExplorationCardType.RELIC_FRAGMENT,
                    "Purge this card to draw 1 relic",
                ),
            ],
            PlanetTrait.INDUSTRIAL: [
                (
                    "Mining World",
                    ExplorationCardType.NORMAL,
                    "Gain 2 trade goods",
                ),
                (
                    "Industrial Complex",
                    ExplorationCardType.ATTACHMENT,
                    "This planet provides +1 resource",
                ),
                (
                    "Relic Fragment",
                    ExplorationCardType.RELIC_FRAGMENT,
                    "Purge this card to draw 1 relic",
                ),
            ],
            PlanetTrait.FRONTIER: [
                (
                    "Ion Storm",
                    ExplorationCardType.NORMAL,
                    "Each ship in this system sustains 1 hit",
                ),
                (
                    "Derelict Vessel",
                    ExplorationCardType.NORMAL,
                    "Gain 2 trade goods",
                ),
                (
                    "Relic Fragment",
                    ExplorationCardType.RELIC_FRAGMENT,
                    "Purge this card to draw 1 relic",
                ),
            ],
        }

        if self.trait in deck_configs:
            self.cards = [
                ExplorationCard(name, self.trait, card_type, effect)
                for name, card_type, effect in deck_configs[self.trait]
            ]

    def draw_card(self) -> ExplorationCard | None:
        """Draw a card from the deck, reshuffling if necessary.

        LRR 35.7a: If there are no cards in an exploration deck, its discard
        pile is shuffled to form a new exploration deck.
        """
        if not self.cards and self.discard_pile:
            self._reshuffle_deck()

        if self.cards:
            return self.cards.pop(0)
        return None

    def _reshuffle_deck(self) -> None:
        """Reshuffle discard pile into deck (Rule 35.7a)."""
        self.cards = self.discard_pile.copy()
        self.discard_pile.clear()
        random.shuffle(self.cards)

    def discard_card(self, card: ExplorationCard) -> None:
        """Add a card to the discard pile."""
        self.discard_pile.append(card)


class ExplorationSystem:
    """Manages the exploration system according to Rule 35."""

    def __init__(self) -> None:
        self.decks: dict[PlanetTrait, ExplorationDeck] = self._initialize_decks()

    def _initialize_decks(self) -> dict[PlanetTrait, ExplorationDeck]:
        """Initialize all exploration decks."""
        return {
            PlanetTrait.CULTURAL: ExplorationDeck(PlanetTrait.CULTURAL),
            PlanetTrait.HAZARDOUS: ExplorationDeck(PlanetTrait.HAZARDOUS),
            PlanetTrait.INDUSTRIAL: ExplorationDeck(PlanetTrait.INDUSTRIAL),
            PlanetTrait.FRONTIER: ExplorationDeck(PlanetTrait.FRONTIER),
        }

    def should_trigger_exploration(
        self, planet: Planet, previous_controller: str | None = None
    ) -> bool:
        """Determine if exploration should be triggered for a planet.

        LRR 35.1: When a player takes control of a planet that is not already
        controlled by another player, they explore that planet.

        LRR 35.2b: Planets that do not have traits cannot be explored.
        """
        # No exploration if planet has no traits (Rule 35.2b)
        if not planet.traits:
            return False

        # No exploration if planet was already controlled by another player
        if previous_controller is not None:
            return False

        return True

    def explore_planet(
        self,
        player: Player,
        planet: Planet,
        game_state: GameState,
        chosen_trait: PlanetTrait | None = None,
        force_exploration: bool = False,
        previous_controller: str | None = None,
    ) -> ExplorationResult:
        """Explore a planet according to Rule 35.

        Args:
            player: The player exploring
            planet: The planet being explored
            game_state: Current game state
            chosen_trait: For multi-trait planets, the chosen trait (Rule 35.2c)
            force_exploration: Force exploration even if normally not allowed (Rule 35.3)
            previous_controller: The previous controller of the planet (if any)
        """
        result = ExplorationResult(success=True, planet_name=planet.name)

        # Check if exploration should be triggered
        if not force_exploration and not self.should_trigger_exploration(
            planet, previous_controller
        ):
            result.exploration_triggered = False
            return result

        # Determine which deck to use (Rule 35.2c for multiple traits)
        # Convert string traits to PlanetTrait enums
        trait_enums: list[PlanetTrait] = []
        for trait in planet.traits:
            if isinstance(trait, PlanetTrait):
                trait_enums.append(trait)
            elif isinstance(trait, str) and trait in [t.value for t in PlanetTrait]:
                trait_enums.append(PlanetTrait(trait))

        # If no valid traits found, return early
        if not trait_enums:
            result.exploration_triggered = False
            return result

        deck_trait = self._determine_exploration_deck(trait_enums, chosen_trait)

        result.exploration_triggered = True
        result.deck_used = deck_trait

        # Draw and resolve card
        card = self._draw_exploration_card(deck_trait)
        if card:
            result.card_drawn = card
            card_result = self.resolve_exploration_card(
                card, player, planet, game_state
            )
            self._merge_card_results(result, card_result)

        return result

    def _determine_exploration_deck(
        self, planet_traits: list[PlanetTrait], chosen_trait: PlanetTrait | None
    ) -> PlanetTrait:
        """Determine which exploration deck to use based on planet traits."""
        if not planet_traits:
            raise ValueError(
                "Cannot determine exploration deck for planet with no valid traits"
            )

        if chosen_trait and chosen_trait in planet_traits:
            return chosen_trait
        elif len(planet_traits) == 1:
            return planet_traits[0]
        else:
            # For multiple traits, default to first trait (in real game, player chooses)
            return planet_traits[0]

    def _draw_exploration_card(self, deck_trait: PlanetTrait) -> ExplorationCard | None:
        """Draw a card from the appropriate exploration deck."""
        deck = self.decks[deck_trait]
        return deck.draw_card()

    def _merge_card_results(
        self, main_result: ExplorationResult, card_result: ExplorationResult
    ) -> None:
        """Merge card resolution results into main exploration result."""
        main_result.card_discarded = card_result.card_discarded
        main_result.card_attached = card_result.card_attached
        main_result.relic_fragment_gained = card_result.relic_fragment_gained
        main_result.effect_applied = card_result.effect_applied

    def explore_multiple_planets(
        self, player: Player, planets: list[Planet], game_state: GameState
    ) -> list[ExplorationResult]:
        """Explore multiple planets in order (Rule 35.2d).

        LRR 35.2d: If a player gains control of multiple planets or resolves
        multiple explore effects at the same time, they choose the order in which
        to resolve them.
        """
        return [self.explore_planet(player, planet, game_state) for planet in planets]

    def explore_frontier_token(
        self,
        player: Player,
        system: Any,  # Mock system object for testing
        game_state: GameState,
    ) -> ExplorationResult:
        """Explore a frontier token (Rule 35.4-35.6).

        LRR 35.4: Players can explore space areas that contain frontier tokens
        if they own the "Dark Energy Tap" technology or if another game effect
        allows them to.

        LRR 35.5: When a player explores a frontier token, they draw and resolve
        a card from the frontier exploration deck.

        LRR 35.6: After a frontier token is explored, it is discarded and
        returned to the supply.
        """
        result = ExplorationResult(success=True)

        if not self._has_frontier_token(system):
            result.success = False
            return result

        # Rule 35.4: Check if player can explore frontier tokens
        if not self._can_explore_frontier_tokens(player, game_state):
            result.success = False
            result.exploration_triggered = False
            return result

        result.exploration_triggered = True
        result.deck_used = PlanetTrait.FRONTIER

        # Draw from frontier deck
        card = self.decks[PlanetTrait.FRONTIER].draw_card()
        if card:
            result.card_drawn = card
            card_result = self.resolve_exploration_card(card, player, None, game_state)
            self._merge_card_results(result, card_result)

        # Remove frontier token (Rule 35.6)
        self._remove_frontier_token(system)
        result.frontier_token_removed = True

        return result

    def _has_frontier_token(self, system: Any) -> bool:
        """Check if system has a frontier token."""
        return hasattr(system, "has_frontier_token") and system.has_frontier_token

    def _remove_frontier_token(self, system: Any) -> None:
        """Remove frontier token from system."""
        if hasattr(system, "remove_frontier_token"):
            system.remove_frontier_token()

    def _can_explore_frontier_tokens(
        self, player: Player, game_state: GameState
    ) -> bool:
        """Check if player can explore frontier tokens (Rule 35.4).

        LRR 35.4: Players can explore space areas that contain frontier tokens
        if they own the "Dark Energy Tap" technology or if another game effect
        allows them to.
        """
        from ti4.core.constants import Technology

        tech_manager = getattr(game_state, "technology_manager", None)
        if tech_manager is None:
            # If no technology manager, assume exploration is not allowed
            return False
        player_technologies = tech_manager.get_player_technologies(player.id)

        # Check if player has Dark Energy Tap technology
        return Technology.DARK_ENERGY_TAP in player_technologies

    def resolve_exploration_card(
        self,
        card: ExplorationCard,
        player: Player,
        planet: Planet | None = None,
        game_state: GameState | None = None,
    ) -> ExplorationResult:
        """Resolve an exploration card (Rule 35.7-35.9).

        LRR 35.7: To resolve an exploration card, a player reads the card, makes
        any necessary decisions, and resolves its ability. If the card was not a
        relic fragment or attachment, it is discarded.
        """
        result = ExplorationResult(success=True)

        if card.is_attachment:
            result = self._resolve_attachment_card(card, planet)
        elif card.is_relic_fragment:
            result = self._resolve_relic_fragment_card(card, player)
        else:
            result = self._resolve_normal_card(card)

        return result

    def _resolve_attachment_card(
        self, card: ExplorationCard, planet: Planet | None
    ) -> ExplorationResult:
        """Resolve an attachment card (Rule 35.8)."""
        result = ExplorationResult(success=True, effect_applied=True)

        if planet:
            if not hasattr(planet, "attached_cards"):
                planet.attached_cards = []
            planet.attached_cards.append(card)
            result.card_attached = True

        return result

    def _resolve_relic_fragment_card(
        self, card: ExplorationCard, player: Player
    ) -> ExplorationResult:
        """Resolve a relic fragment card (Rule 35.9)."""
        result = ExplorationResult(success=True, effect_applied=True)

        # Player.relic_fragments is a mutable list field, we can append to it
        player.relic_fragments.append(card)
        result.relic_fragment_gained = True

        return result

    def _resolve_normal_card(self, card: ExplorationCard) -> ExplorationResult:
        """Resolve a normal exploration card."""
        result = ExplorationResult(
            success=True, effect_applied=True, card_discarded=True
        )

        # Add to discard pile
        if card.trait in self.decks:
            self.decks[card.trait].discard_card(card)

        return result

    def resolve_relic_fragment_ability(
        self, fragment: ExplorationCard, player: Player, game_state: GameState
    ) -> ExplorationResult:
        """Resolve a relic fragment ability (Rule 35.9a).

        LRR 35.9a: Players can resolve the ability of relic fragments that are
        in their play area. Resolving these abilities allows players to draw
        additional exploration cards.
        """
        result = ExplorationResult(success=True)

        if fragment in player.relic_fragments:
            # Remove (purge) the fragment
            player.relic_fragments.remove(fragment)

            # Draw relic (simulated)
            result.relic_drawn = True
            result.effect_applied = True

        return result

    def can_trade_relic_fragment(
        self, fragment: ExplorationCard, player: Player
    ) -> bool:
        """Check if a relic fragment can be traded (Rule 35.9b).

        LRR 35.9b: Relic fragments can be exchanged as part of transactions.
        """
        return fragment in player.relic_fragments
