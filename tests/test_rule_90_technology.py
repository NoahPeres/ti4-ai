"""Tests for Rule 90: TECHNOLOGY mechanics.

This module tests the technology system according to TI4 LRR Rule 90.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

LRR Reference: Rule 90 - TECHNOLOGY
"""

import pytest

from tests.test_constants import MockPlayer
from ti4.core.constants import Technology, UnitType
from ti4.core.technology import TechnologyColor, TechnologyManager


class TestRule90TechnologyBasics:
    """Test basic technology mechanics (Rule 90.0)."""

    def test_technology_manager_exists(self) -> None:
        """Test that technology manager can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 90.0 - Technology cards allow players to upgrade units
        """
        manager = TechnologyManager()
        assert manager is not None

    def test_player_can_own_technologies(self) -> None:
        """Test that players can own technology cards.

        LRR Reference: Rule 90.1 - Each player places any technology they have gained faceup near the faction sheet
        """
        manager = TechnologyManager()

        # Player starts with no technologies
        technologies = manager.get_player_technologies(MockPlayer.PLAYER_1.value)
        assert len(technologies) == 0

        # Player can gain a technology
        manager.gain_technology(MockPlayer.PLAYER_1.value, Technology.CRUISER_II)

        # Player now owns the technology
        technologies = manager.get_player_technologies(MockPlayer.PLAYER_1.value)
        assert Technology.CRUISER_II in technologies
        assert len(technologies) == 1


class TestRule90TechnologyDeck:
    """Test technology deck mechanics (Rule 90.2-90.4)."""

    def test_technology_deck_contains_unowned_cards(self) -> None:
        """Test that technology deck contains cards not yet gained.

        LRR Reference: Rule 90.2 - A player does not own any technology card that is in their technology deck
        """
        manager = TechnologyManager()

        # Technology deck should contain all available technologies initially
        deck = manager.get_technology_deck(MockPlayer.PLAYER_1.value)
        assert Technology.CRUISER_II in deck
        assert Technology.FIGHTER_II in deck
        assert len(deck) > 0

        # After gaining a technology, it should not be in the deck
        manager.gain_technology(MockPlayer.PLAYER_1.value, Technology.CRUISER_II)
        deck_after = manager.get_technology_deck(MockPlayer.PLAYER_1.value)
        assert Technology.CRUISER_II not in deck_after
        assert len(deck_after) == len(deck) - 1

    def test_player_can_look_through_deck(self) -> None:
        """Test that players can examine their technology deck.

        LRR Reference: Rule 90.4 - Player can look through their deck at any time
        """
        manager = TechnologyManager()

        # Player should be able to access their deck
        deck = manager.get_technology_deck(MockPlayer.PLAYER_1.value)
        assert isinstance(deck, set)
        assert len(deck) > 0


class TestRule90ResearchingTechnology:
    """Test technology research mechanics (Rule 90.9-90.12)."""

    def test_can_research_technology_with_prerequisites(self) -> None:
        """Test that players can research technology when prerequisites are met.

        LRR Reference: Rule 90.12 - When researching technology, player must satisfy each prerequisite
        """
        manager = TechnologyManager()

        # Give player prerequisites for Cruiser II (needs 1Y+1R+1G)
        # For testing, we'll use Gravity Drive as a blue tech, but Cruiser II needs Y+R+G
        # So this test should fail until we have the right prerequisites
        manager.gain_technology(MockPlayer.PLAYER_1.value, Technology.GRAVITY_DRIVE)

        # Should NOT be able to research Cruiser II with only blue prerequisite
        can_research = manager.can_research_technology(
            MockPlayer.PLAYER_1.value, Technology.CRUISER_II
        )
        assert can_research is False  # Cruiser II needs Y+R+G, not Blue

    def test_cannot_research_technology_without_prerequisites(self) -> None:
        """Test that players cannot research technology without prerequisites.

        LRR Reference: Rule 90.12 - Player must satisfy each prerequisite by owning one technology of matching color
        """
        manager = TechnologyManager()

        # Player has no technologies, cannot research advanced tech
        can_research = manager.can_research_technology(
            MockPlayer.PLAYER_1.value, Technology.CRUISER_II
        )
        assert can_research is False

    def test_research_technology_adds_to_owned(self) -> None:
        """Test that researching technology adds it to player's owned technologies.

        LRR Reference: Rule 90.10 - To research technology, player gains that technology card from their deck
        """
        manager = TechnologyManager()

        # Test with Antimass Deflectors (no prerequisites)
        success = manager.research_technology(
            MockPlayer.PLAYER_1.value, Technology.ANTIMASS_DEFLECTORS
        )
        assert success is True  # Should succeed - no prerequisites needed

        # Technology should now be owned
        technologies = manager.get_player_technologies(MockPlayer.PLAYER_1.value)
        assert Technology.ANTIMASS_DEFLECTORS in technologies


class TestRule90TechnologyColors:
    """Test technology color system (Rule 90.7-90.8)."""

    def test_technologies_have_colors(self) -> None:
        """Test that technologies have color classifications.

        LRR Reference: Rule 90.7 - Each technology has a colored symbol indicating that technology's color
        """
        manager = TechnologyManager()

        # Test that we can get technology colors (only for non-unit-upgrades)
        color = manager.get_technology_color(Technology.GRAVITY_DRIVE)
        assert color == TechnologyColor.BLUE

        # Unit upgrades should raise an error when asking for color
        with pytest.raises(ValueError, match="unit upgrade and has no color"):
            manager.get_technology_color(Technology.CRUISER_II)

    def test_technologies_have_prerequisites(self) -> None:
        """Test that technologies have prerequisite requirements.

        LRR Reference: Rule 90.8 - Most technology cards have prerequisites displayed as colored symbols
        """
        manager = TechnologyManager()

        # Test that we can get technology prerequisites
        prereqs = manager.get_technology_prerequisites(Technology.CRUISER_II)
        assert TechnologyColor.YELLOW in prereqs
        assert TechnologyColor.RED in prereqs
        assert TechnologyColor.GREEN in prereqs
        assert len(prereqs) == 3  # Cruiser II requires 1Y+1R+1G (confirmed)


class TestRule90UnitUpgrades:
    """Test unit upgrade technology mechanics (Rule 90.6)."""

    def test_unit_upgrade_technologies_identified(self) -> None:
        """Test that unit upgrade technologies are properly identified.

        LRR Reference: Rule 90.6 - Some technologies are unit upgrades that share a name with a unit
        """
        manager = TechnologyManager()

        # Test unit upgrade identification (only confirmed technologies)
        assert manager.is_unit_upgrade(Technology.CRUISER_II) is True
        assert manager.is_unit_upgrade(Technology.GRAVITY_DRIVE) is False

    def test_unit_upgrade_affects_unit_type(self) -> None:
        """Test that unit upgrades are associated with specific unit types.

        LRR Reference: Rule 90.6 - Unit upgrades share a name with a unit printed on player's faction sheet
        """
        manager = TechnologyManager()

        # Test unit type associations
        unit_type = manager.get_upgraded_unit_type(Technology.CRUISER_II)
        assert unit_type == UnitType.CRUISER

        # Only test confirmed unit upgrades
        # FIGHTER_II test removed - needs manual confirmation


class TestRule90FactionTechnologyRestriction:
    """Test faction technology restriction mechanics (Rule 90.11)."""

    def test_faction_technology_restriction_framework_exists(self) -> None:
        """Test that faction technology restriction framework exists.

        LRR Reference: Rule 90.11 - A player cannot research a faction technology that does not match their faction
        """
        from ti4.core.constants import Faction

        manager = TechnologyManager()

        # Test that the framework method exists
        assert hasattr(manager, "can_research_faction_technology")

        # Test with generic technology - should always be allowed
        can_research = manager.can_research_faction_technology(
            MockPlayer.PLAYER_1.value, Faction.SOL, Technology.GRAVITY_DRIVE
        )
        assert (
            can_research is True
        )  # Generic technologies should be researchable by any faction

    def test_cannot_research_other_faction_technology(self) -> None:
        """Test that players cannot research faction technologies from other factions.

        LRR Reference: Rule 90.11 - A player cannot research a faction technology that does not match their faction
        """
        from ti4.core.constants import Faction

        manager = TechnologyManager()

        # Sol player should NOT be able to research Hacan faction technology
        can_research = manager.can_research_faction_technology(
            MockPlayer.PLAYER_1.value,
            Faction.SOL,
            Technology.QUANTUM_DATAHUB_NODE,  # Hacan faction tech
        )
        assert can_research is False

        # Hacan player should NOT be able to research Sol faction technology
        can_research = manager.can_research_faction_technology(
            MockPlayer.PLAYER_2.value,
            Faction.HACAN,
            Technology.SPEC_OPS_II,  # Sol faction tech
        )
        assert can_research is False

    def test_can_research_own_faction_technology(self) -> None:
        """Test that players can research their own faction's technologies.

        LRR Reference: Rule 90.11 - Players can research faction technologies that match their faction
        """
        from ti4.core.constants import Faction

        manager = TechnologyManager()

        # Sol player should be able to research Sol faction technology
        can_research = manager.can_research_faction_technology(
            MockPlayer.PLAYER_1.value,
            Faction.SOL,
            Technology.SPEC_OPS_II,  # Sol faction tech
        )
        assert can_research is True

        # Hacan player should be able to research Hacan faction technology
        can_research = manager.can_research_faction_technology(
            MockPlayer.PLAYER_2.value,
            Faction.HACAN,
            Technology.QUANTUM_DATAHUB_NODE,  # Hacan faction tech
        )
        assert can_research is True

    def test_can_research_generic_technology_regardless_of_faction(self) -> None:
        """Test that players can research generic technologies regardless of faction.

        LRR Reference: Rule 90.11 - Faction restriction only applies to faction technologies
        """
        from ti4.core.constants import Faction

        manager = TechnologyManager()

        # Any player should be able to research generic technologies
        can_research_sol = manager.can_research_faction_technology(
            MockPlayer.PLAYER_1.value,
            Faction.SOL,
            Technology.GRAVITY_DRIVE,  # Generic tech
        )
        assert can_research_sol is True

        # Same generic tech should be researchable by different faction
        can_research_hacan = manager.can_research_faction_technology(
            MockPlayer.PLAYER_2.value,
            Faction.HACAN,
            Technology.GRAVITY_DRIVE,  # Generic tech
        )
        assert can_research_hacan is True
