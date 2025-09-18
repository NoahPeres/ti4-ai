"""Tests for technology system."""

from src.ti4.core.game_state_manager import GameState
from src.ti4.core.player import Player
from src.ti4.core.technology import Technology, TechnologyColor, TechnologyTree


class TestTechnology:
    """Test technology creation and validation."""

    def test_technology_creation(self) -> None:
        """Test that a technology can be created with basic properties."""
        tech = Technology(
            name="Gravity Drive", color=TechnologyColor.BLUE, prerequisites=[]
        )
        assert tech.name == "Gravity Drive"
        assert tech.color == TechnologyColor.BLUE
        assert tech.prerequisites == []

    def test_technology_with_prerequisites(self) -> None:
        """Test that a technology can be created with prerequisites."""
        tech = Technology(
            name="Dreadnought II",
            color=TechnologyColor.RED,
            prerequisites=["Dreadnought", "Red Tech"],
        )
        assert tech.name == "Dreadnought II"
        assert tech.color == TechnologyColor.RED
        assert tech.prerequisites == ["Dreadnought", "Red Tech"]


class TestTechnologyTree:
    """Test technology tree navigation and validation."""

    def test_technology_tree_creation(self) -> None:
        """Test that a technology tree can be created."""
        tree = TechnologyTree()
        assert tree is not None

    def test_can_research_technology_no_prerequisites(self) -> None:
        """Test that a technology with no prerequisites can be researched."""
        tree = TechnologyTree()
        tech = Technology(
            name="Antimass Deflectors", color=TechnologyColor.BLUE, prerequisites=[]
        )
        player_technologies: list[str] = []

        result = tree.can_research(tech, player_technologies)
        assert result is True

    def test_cannot_research_technology_missing_prerequisites(self) -> None:
        """Test that a technology with missing prerequisites cannot be researched."""
        tree = TechnologyTree()
        tech = Technology(
            name="Dreadnought II",
            color=TechnologyColor.RED,
            prerequisites=["Dreadnought"],
        )
        player_technologies: list[str] = []  # Player has no technologies

        result = tree.can_research(tech, player_technologies)
        assert result is False

    def test_can_research_technology_with_satisfied_prerequisites(self) -> None:
        """Test that a technology can be researched when prerequisites are satisfied."""
        tree = TechnologyTree()
        tech = Technology(
            name="Dreadnought II",
            color=TechnologyColor.RED,
            prerequisites=["Dreadnought"],
        )
        player_technologies = ["Dreadnought"]  # Player has the prerequisite

        result = tree.can_research(tech, player_technologies)
        assert result is True

    def test_can_research_technology_with_multiple_prerequisites(self) -> None:
        """Test that a technology with multiple prerequisites can be researched when all are satisfied."""
        tree = TechnologyTree()
        tech = Technology(
            name="War Sun",
            color=TechnologyColor.RED,
            prerequisites=["Dreadnought II", "Advanced Weaponry"],
        )
        player_technologies = ["Dreadnought II", "Advanced Weaponry"]

        result = tree.can_research(tech, player_technologies)
        assert result is True

    def test_cannot_research_technology_with_partial_prerequisites(self) -> None:
        """Test that a technology cannot be researched when only some prerequisites are satisfied."""
        tree = TechnologyTree()
        tech = Technology(
            name="War Sun",
            color=TechnologyColor.RED,
            prerequisites=["Dreadnought II", "Advanced Weaponry"],
        )
        player_technologies = ["Dreadnought II"]  # Missing "Advanced Weaponry"

        result = tree.can_research(tech, player_technologies)
        assert result is False


class TestTechnologyGainEffects:
    """Test technology gain effects and validation."""

    def test_research_technology_action_validates_prerequisites(self) -> None:
        """Test that researching a technology validates prerequisites are met."""
        # RED: This test should fail because ResearchTechnologyAction doesn't exist yet
        from src.ti4.actions.research_technology import ResearchTechnologyAction

        # Create a game state with a player who has some technologies
        game_state = GameState()
        player = Player(id="player1", faction="Sol")
        game_state.add_player(player)
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        player_state.technologies.add("Antimass Deflectors")

        # Create a technology that requires prerequisites
        tech = Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Create research action
        action = ResearchTechnologyAction(technology=tech)

        # Should be legal since player has prerequisites
        assert action.is_legal(game_state, "player1") is True

    def test_research_technology_action_rejects_missing_prerequisites(self) -> None:
        """Test that researching a technology is rejected when prerequisites are missing."""
        from src.ti4.actions.research_technology import ResearchTechnologyAction

        # Create a game state with a player who has no technologies
        game_state = GameState()
        player = Player(id="player1", faction="Sol")
        game_state.add_player(player)

        # Create a technology that requires prerequisites
        tech = Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Create research action
        action = ResearchTechnologyAction(technology=tech)

        # Should be illegal since player lacks prerequisites
        assert action.is_legal(game_state, "player1") is False

    def test_research_technology_action_adds_technology_to_player(self) -> None:
        """Test that executing a research action adds the technology to the player's collection."""
        from src.ti4.actions.research_technology import ResearchTechnologyAction

        # Create a game state with a player who has prerequisites
        game_state = GameState()
        player = Player(id="player1", faction="Sol")
        game_state.add_player(player)
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        player_state.technologies.add("Antimass Deflectors")

        # Create a technology that requires prerequisites
        tech = Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Create and execute research action
        action = ResearchTechnologyAction(technology=tech)
        new_state = action.execute(game_state, "player1")

        # Technology should be added to player's collection
        new_player_state = new_state.get_player_state("player1")
        assert "Gravity Drive" in new_player_state.technologies

    def test_research_technology_action_raises_error_on_illegal_execution(self) -> None:
        """Test that executing an illegal research action raises an error."""
        from src.ti4.actions.research_technology import ResearchTechnologyAction

        # Create a game state with a player who lacks prerequisites
        game_state = GameState()
        player = Player(id="player1", faction="Sol")
        game_state.add_player(player)

        # Create a technology that requires prerequisites
        tech = Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Create research action
        action = ResearchTechnologyAction(technology=tech)

        # Should raise an error when executed
        try:
            action.execute(game_state, "player1")
            assert False, "Expected ValueError to be raised"
        except ValueError as e:
            assert "Cannot research Gravity Drive: prerequisites not met" in str(e)


class TestTechnologyEffects:
    """Test technology effects on game mechanics."""

    def test_technology_effects_are_applied_to_units(self) -> None:
        """Test that technology effects are applied to unit stats."""
        # RED: This test should fail because TechnologyEffectSystem doesn't exist yet
        from src.ti4.core.technology import TechnologyEffectSystem
        from src.ti4.core.unit import Unit
        from src.ti4.core.unit_stats import UnitStats

        # Create a technology with effects (not used directly in this test)
        Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Create an effect system and register the technology effect
        effect_system = TechnologyEffectSystem()
        effect_system.register_technology_effect(
            technology_name="Gravity Drive",
            unit_type="destroyer",
            stat_modifier=UnitStats(movement=1),  # +1 movement
        )

        # Create a unit and apply technology effects using the same stats provider
        unit = Unit(
            unit_type="destroyer",
            owner="player1",
            technologies={"Gravity Drive"},
            stats_provider=effect_system._unit_stats_provider,
        )

        # The unit should have the technology effect applied
        stats = unit.get_stats()
        base_destroyer_movement = 2  # Base destroyer movement
        expected_movement = base_destroyer_movement + 1  # +1 from Gravity Drive
        assert stats.movement == expected_movement

    def test_technology_effects_triggered_by_research_action(self) -> None:
        """Test that technology effects are applied when a technology is researched."""
        from src.ti4.actions.research_technology import ResearchTechnologyAction
        from src.ti4.core.technology import TechnologyEffectSystem
        from src.ti4.core.unit import Unit
        from src.ti4.core.unit_stats import UnitStats

        # Create a game state with a player who has prerequisites
        game_state = GameState()
        player = Player(id="player1", faction="Sol")
        game_state.add_player(player)
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        player_state.technologies.add("Antimass Deflectors")

        # Create a technology with effects
        gravity_drive = Technology(
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=["Antimass Deflectors"],
        )

        # Set up the effect system in the game state
        effect_system = TechnologyEffectSystem(game_state.unit_stats_provider)
        effect_system.register_technology_effect(
            technology_name="Gravity Drive",
            unit_type="destroyer",
            stat_modifier=UnitStats(movement=1),  # +1 movement
        )

        # Research the technology
        action = ResearchTechnologyAction(technology=gravity_drive)
        new_state = action.execute(game_state, "player1")

        # Verify the technology was added
        new_player_state = new_state.get_player_state("player1")
        assert "Gravity Drive" in new_player_state.technologies

        # Create a unit with the new technology and verify effects are applied
        unit = Unit(
            unit_type="destroyer",
            owner="player1",
            technologies=new_player_state.technologies,
            stats_provider=new_state.unit_stats_provider,
        )

        stats = unit.get_stats()
        base_destroyer_movement = 2  # Base destroyer movement
        expected_movement = base_destroyer_movement + 1  # +1 from Gravity Drive
        assert stats.movement == expected_movement
