import functools

from ti4.core.abilities import Ability, AbilityCost, AbilityEffect, TimingWindow
from ti4.core.card_types import PlanetTrait
from ti4.core.exploration import ExplorationCard, ExplorationCardType


def _make_relic_fragment_of_trait(trait: PlanetTrait) -> ExplorationCard:
    return ExplorationCard(
        name=f"{trait.name} Relic Fragment",
        trait=trait,
        card_type=ExplorationCardType.RELIC_FRAGMENT,
        effect=f"ACTION: Purge 3 of your {trait.name.lower()} relic fragments to gain 1 Relic.",
        ability=Ability(
            name=f"{trait.name.lower()}_relic_fragments",
            timing=TimingWindow.ACTION,
            trigger="player_action",
            effect=AbilityEffect(type="draw", value="relic_deck"),
            cost=AbilityCost(
                type=f"purge_{trait.name.lower()}_relic_fragments", amount=3
            ),
        ),
    )


make_hazardous_relic_fragment = functools.partial(
    _make_relic_fragment_of_trait, PlanetTrait.HAZARDOUS
)
make_cultural_relic_fragment = functools.partial(
    _make_relic_fragment_of_trait, PlanetTrait.CULTURAL
)
make_industrial_relic_fragment = functools.partial(
    _make_relic_fragment_of_trait, PlanetTrait.INDUSTRIAL
)


def make_unknown_relic_fragment() -> ExplorationCard:
    return ExplorationCard(
        name="Unknown Relic Fragment",
        trait=PlanetTrait.FRONTIER,
        card_type=ExplorationCardType.RELIC_FRAGMENT,
        effect="This card counts as a relic fragment of any type.",
    )
