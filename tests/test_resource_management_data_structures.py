"""Tests for resource management data structures.

Tests the core data structures for Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.
"""

from src.ti4.core.constants import UnitType
from src.ti4.core.resource_management import (
    InfluenceSources,
    InfluenceSpending,
    ProductionCost,
    ResourceSources,
    ResourceSpending,
    SpendingPlan,
)


class TestResourceSources:
    """Test ResourceSources dataclass for resource breakdown tracking."""

    def test_resource_sources_creation(self) -> None:
        """Test creating ResourceSources with planet and trade goods data."""
        planets = {"Mecatol Rex": 1, "Jord": 4}
        trade_goods = 3
        total = 8

        sources = ResourceSources(
            planets=planets, trade_goods=trade_goods, total_available=total
        )

        assert sources.planets == planets
        assert sources.trade_goods == trade_goods
        assert sources.total_available == total

    def test_get_planet_names(self) -> None:
        """Test getting planet names from resource sources."""
        planets = {"Mecatol Rex": 1, "Jord": 4, "Muaat": 2}
        sources = ResourceSources(planets=planets, trade_goods=0, total_available=7)

        planet_names = sources.get_planet_names()
        assert set(planet_names) == {"Mecatol Rex", "Jord", "Muaat"}


class TestInfluenceSources:
    """Test InfluenceSources dataclass for influence breakdown tracking."""

    def test_influence_sources_creation(self) -> None:
        """Test creating InfluenceSources with planet and trade goods data."""
        planets = {"Mecatol Rex": 6, "Jord": 2}
        trade_goods = 2
        total = 10

        sources = InfluenceSources(
            planets=planets,
            trade_goods=trade_goods,
            total_available=total,
            for_voting=False,
        )

        assert sources.planets == planets
        assert sources.trade_goods == trade_goods
        assert sources.total_available == total
        assert sources.for_voting is False

    def test_influence_sources_for_voting_no_trade_goods(self) -> None:
        """Test that trade goods are 0 when for_voting=True (Rule 47.3)."""
        planets = {"Mecatol Rex": 6, "Jord": 2}

        sources = InfluenceSources(
            planets=planets,
            trade_goods=0,  # Must be 0 for voting
            total_available=8,
            for_voting=True,
        )

        assert sources.trade_goods == 0
        assert sources.for_voting is True

    def test_get_planet_names(self) -> None:
        """Test getting planet names from influence sources."""
        planets = {"Mecatol Rex": 6, "Jord": 2, "Muaat": 1}
        sources = InfluenceSources(
            planets=planets, trade_goods=1, total_available=10, for_voting=False
        )

        planet_names = sources.get_planet_names()
        assert set(planet_names) == {"Mecatol Rex", "Jord", "Muaat"}


class TestResourceSpending:
    """Test ResourceSpending dataclass for resource spending details."""

    def test_resource_spending_creation(self) -> None:
        """Test creating ResourceSpending with planets and trade goods."""
        planets_to_exhaust = {"Jord": 4, "Muaat": 2}
        trade_goods_to_spend = 1
        total_resources = 7

        spending = ResourceSpending(
            planets_to_exhaust=planets_to_exhaust,
            trade_goods_to_spend=trade_goods_to_spend,
            total_resources=total_resources,
        )

        assert spending.planets_to_exhaust == planets_to_exhaust
        assert spending.trade_goods_to_spend == trade_goods_to_spend
        assert spending.total_resources == total_resources


class TestInfluenceSpending:
    """Test InfluenceSpending dataclass for influence spending details."""

    def test_influence_spending_creation(self) -> None:
        """Test creating InfluenceSpending with planets and trade goods."""
        planets_to_exhaust = {"Mecatol Rex": 6, "Jord": 2}
        trade_goods_to_spend = 2
        total_influence = 10

        spending = InfluenceSpending(
            planets_to_exhaust=planets_to_exhaust,
            trade_goods_to_spend=trade_goods_to_spend,
            total_influence=total_influence,
        )

        assert spending.planets_to_exhaust == planets_to_exhaust
        assert spending.trade_goods_to_spend == trade_goods_to_spend
        assert spending.total_influence == total_influence

    def test_influence_spending_for_voting_no_trade_goods(self) -> None:
        """Test influence spending for voting with no trade goods (Rule 47.3)."""
        planets_to_exhaust = {"Mecatol Rex": 6, "Jord": 2}

        spending = InfluenceSpending(
            planets_to_exhaust=planets_to_exhaust,
            trade_goods_to_spend=0,  # No trade goods for voting
            total_influence=8,
        )

        assert spending.trade_goods_to_spend == 0
        assert spending.total_influence == 8


class TestSpendingPlan:
    """Test SpendingPlan dataclass for spending operations."""

    def test_spending_plan_creation(self) -> None:
        """Test creating a valid SpendingPlan."""
        resource_spending = ResourceSpending(
            planets_to_exhaust={"Jord": 4}, trade_goods_to_spend=1, total_resources=5
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={"Mecatol Rex": 6},
            trade_goods_to_spend=0,
            total_influence=6,
        )

        plan = SpendingPlan(
            player_id="player1",
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=5,
            total_influence_cost=6,
            is_valid=True,
        )

        assert plan.player_id == "player1"
        assert plan.resource_spending == resource_spending
        assert plan.influence_spending == influence_spending
        assert plan.total_resource_cost == 5
        assert plan.total_influence_cost == 6
        assert plan.is_valid is True
        assert plan.error_message is None

    def test_spending_plan_invalid_with_error(self) -> None:
        """Test creating an invalid SpendingPlan with error message."""
        resource_spending = ResourceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_resources=0
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
        )

        plan = SpendingPlan(
            player_id="player1",
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=5,
            total_influence_cost=0,
            is_valid=False,
            error_message="Insufficient resources: need 5, have 0",
        )

        assert plan.is_valid is False
        assert plan.error_message == "Insufficient resources: need 5, have 0"

    def test_get_total_planets_to_exhaust(self) -> None:
        """Test getting all planets that will be exhausted by the plan."""
        resource_spending = ResourceSpending(
            planets_to_exhaust={"Jord": 4, "Muaat": 2},
            trade_goods_to_spend=0,
            total_resources=6,
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={"Mecatol Rex": 6, "Jord": 2},  # Jord used for both
            trade_goods_to_spend=0,
            total_influence=8,
        )

        plan = SpendingPlan(
            player_id="player1",
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=6,
            total_influence_cost=8,
            is_valid=True,
        )

        all_planets = plan.get_total_planets_to_exhaust()
        assert all_planets == {"Jord", "Muaat", "Mecatol Rex"}

    def test_get_total_trade_goods_to_spend(self) -> None:
        """Test getting total trade goods that will be consumed."""
        resource_spending = ResourceSpending(
            planets_to_exhaust={"Jord": 4}, trade_goods_to_spend=2, total_resources=6
        )
        influence_spending = InfluenceSpending(
            planets_to_exhaust={"Mecatol Rex": 6},
            trade_goods_to_spend=1,
            total_influence=7,
        )

        plan = SpendingPlan(
            player_id="player1",
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=6,
            total_influence_cost=7,
            is_valid=True,
        )

        total_trade_goods = plan.get_total_trade_goods_to_spend()
        assert total_trade_goods == 3


class TestProductionCost:
    """Test ProductionCost dataclass for production cost calculations."""

    def test_production_cost_creation(self) -> None:
        """Test creating ProductionCost for normal unit production."""
        cost = ProductionCost(
            unit_type=UnitType.CRUISER,
            base_cost=2.0,
            modified_cost=1.5,  # After technology discount
            quantity_requested=1,
            units_produced=1,
            total_cost=1.5,
            is_dual_production=False,
        )

        assert cost.unit_type == UnitType.CRUISER
        assert cost.base_cost == 2.0
        assert cost.modified_cost == 1.5
        assert cost.quantity_requested == 1
        assert cost.units_produced == 1
        assert cost.total_cost == 1.5
        assert cost.is_dual_production is False

    def test_production_cost_dual_production(self) -> None:
        """Test ProductionCost for dual production (Rule 26.2)."""
        cost = ProductionCost(
            unit_type=UnitType.FIGHTER,
            base_cost=0.5,
            modified_cost=0.5,
            quantity_requested=1,
            units_produced=2,  # Dual production produces 2 for cost of 1
            total_cost=0.5,
            is_dual_production=True,
        )

        assert cost.unit_type == UnitType.FIGHTER
        assert cost.quantity_requested == 1
        assert cost.units_produced == 2
        assert cost.is_dual_production is True

    def test_get_cost_per_unit(self) -> None:
        """Test calculating cost per unit actually produced."""
        # Normal production
        normal_cost = ProductionCost(
            unit_type=UnitType.CRUISER,
            base_cost=2.0,
            modified_cost=2.0,
            quantity_requested=1,
            units_produced=1,
            total_cost=2.0,
            is_dual_production=False,
        )
        assert normal_cost.get_cost_per_unit() == 2.0

        # Dual production
        dual_cost = ProductionCost(
            unit_type=UnitType.FIGHTER,
            base_cost=0.5,
            modified_cost=0.5,
            quantity_requested=1,
            units_produced=2,
            total_cost=0.5,
            is_dual_production=True,
        )
        assert dual_cost.get_cost_per_unit() == 0.25  # 0.5 / 2 units
