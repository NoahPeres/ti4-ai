"""Game state machine for managing phase transitions."""


from .game_phase import GamePhase


class GameStateMachine:
    """Manages game phase transitions with validation."""

    def __init__(self):
        """Initialize state machine in SETUP phase."""
        self._current_phase = GamePhase.SETUP
        self._valid_transitions = self._build_transition_map()

    @property
    def current_phase(self) -> GamePhase:
        """Get the current game phase."""
        return self._current_phase

    def can_transition_to(self, new_phase: GamePhase) -> bool:
        """Check if transition to new phase is valid."""
        return new_phase in self._valid_transitions.get(self._current_phase, set())

    def transition_to(self, new_phase: GamePhase) -> None:
        """Transition to new phase if valid."""
        if self.can_transition_to(new_phase):
            self._current_phase = new_phase
        else:
            raise ValueError(
                f"Invalid transition from {self._current_phase} to {new_phase}"
            )

    def get_valid_transitions(self) -> set[GamePhase]:
        """Get all valid transitions from current phase."""
        return self._valid_transitions.get(self._current_phase, set())

    def _build_transition_map(self) -> dict[GamePhase, set[GamePhase]]:
        """Build the valid phase transition map."""
        return {
            GamePhase.SETUP: {GamePhase.STRATEGY},
            GamePhase.STRATEGY: {GamePhase.ACTION},
            GamePhase.ACTION: {GamePhase.STATUS},
            GamePhase.STATUS: {GamePhase.AGENDA},
            GamePhase.AGENDA: {GamePhase.STRATEGY},  # Next round
        }
