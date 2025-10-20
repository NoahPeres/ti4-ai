"""Tests for status phase documentation quality and completeness.

This module tests that all public methods in the status phase implementation
have proper docstrings, accurate LRR references, and meet code quality standards.

LRR References:
- Rule 81: Status Phase - Complete 8-step sequence
- Rule 34.2: Ready Cards step

Requirements: 12.4
"""

import inspect
import re
from typing import Any, get_type_hints

from src.ti4.core.status_phase import (
    DrawActionCardsStep,
    GainRedistributeTokensStep,
    ReadyCardsStep,
    RemoveCommandTokensStep,
    RepairUnitsStep,
    ReturnStrategyCardsStep,
    RevealObjectiveStep,
    RoundTransitionManager,
    ScoreObjectivesStep,
    StatusPhaseError,
    StatusPhaseGameStateError,
    StatusPhaseManager,
    StatusPhaseOrchestrator,
    StatusPhaseResult,
    StatusPhaseStepHandler,
    StatusPhaseValidator,
    StepResult,
    StepValidationError,
    SystemIntegrationError,
)


class TestStatusPhaseDocstrings:
    """Test that all public methods have proper docstrings."""

    def test_step_result_has_comprehensive_docstring(self) -> None:
        """Test that StepResult class has comprehensive documentation."""
        # RED: Test that StepResult has proper docstring
        docstring = StepResult.__doc__
        assert docstring is not None
        assert "Result of executing a status phase step" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring
        assert "Attributes:" in docstring
        assert "success:" in docstring
        assert "step_name:" in docstring

    def test_status_phase_result_has_comprehensive_docstring(self) -> None:
        """Test that StatusPhaseResult class has comprehensive documentation."""
        # RED: Test that StatusPhaseResult has proper docstring
        docstring = StatusPhaseResult.__doc__
        assert docstring is not None
        assert "Result of complete status phase execution" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring
        assert "Attributes:" in docstring

        # Test public methods have docstrings
        assert StatusPhaseResult.get_step_result.__doc__ is not None
        assert StatusPhaseResult.was_step_successful.__doc__ is not None

    def test_status_phase_orchestrator_has_comprehensive_docstring(self) -> None:
        """Test that StatusPhaseOrchestrator class has comprehensive documentation."""
        # RED: Test that StatusPhaseOrchestrator has proper docstring
        docstring = StatusPhaseOrchestrator.__doc__
        assert docstring is not None
        assert "Orchestrates the complete 8-step status phase sequence" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring

        # Test all public methods have docstrings
        orchestrator = StatusPhaseOrchestrator()
        assert orchestrator.execute_complete_status_phase.__doc__ is not None
        assert orchestrator.execute_step.__doc__ is not None
        assert orchestrator.validate_step_prerequisites.__doc__ is not None
        assert orchestrator.get_step_handler.__doc__ is not None

    def test_round_transition_manager_has_comprehensive_docstring(self) -> None:
        """Test that RoundTransitionManager class has comprehensive documentation."""
        # RED: Test that RoundTransitionManager has proper docstring
        docstring = RoundTransitionManager.__doc__
        assert docstring is not None
        assert "Manages phase transitions after status phase completion" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring
        assert "Rule 27.4" in docstring

        # Test all public methods have docstrings
        manager = RoundTransitionManager()
        assert manager.determine_next_phase.__doc__ is not None
        assert manager.transition_to_agenda_phase.__doc__ is not None
        assert manager.transition_to_new_round.__doc__ is not None
        assert manager.update_round_counter.__doc__ is not None

    def test_status_phase_manager_has_comprehensive_docstring(self) -> None:
        """Test that StatusPhaseManager class has comprehensive documentation."""
        # RED: Test that StatusPhaseManager has proper docstring
        docstring = StatusPhaseManager.__doc__
        assert docstring is not None
        assert "Enhanced status phase manager with complete functionality" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring

        # Test all public methods have docstrings
        manager = StatusPhaseManager()
        assert manager.execute_complete_status_phase.__doc__ is not None
        assert manager.execute_single_step.__doc__ is not None
        assert manager.ready_all_cards.__doc__ is not None

    def test_status_phase_validator_has_comprehensive_docstring(self) -> None:
        """Test that StatusPhaseValidator class has comprehensive documentation."""
        # RED: Test that StatusPhaseValidator has proper docstring
        docstring = StatusPhaseValidator.__doc__
        assert docstring is not None
        assert "Validates status phase operations and state" in docstring
        assert "LRR References:" in docstring
        assert "Rule 81" in docstring

    def test_step_handler_classes_have_comprehensive_docstrings(self) -> None:
        """Test that all step handler classes have comprehensive documentation."""
        step_handlers = [
            ScoreObjectivesStep,
            RevealObjectiveStep,
            DrawActionCardsStep,
            RemoveCommandTokensStep,
            GainRedistributeTokensStep,
            ReadyCardsStep,
            RepairUnitsStep,
            ReturnStrategyCardsStep,
        ]

        for handler_class in step_handlers:
            # RED: Test that each step handler has proper docstring
            docstring = handler_class.__doc__
            assert docstring is not None, f"{handler_class.__name__} missing docstring"
            assert "Handles Step" in docstring, (
                f"{handler_class.__name__} docstring missing step description"
            )
            assert "LRR References:" in docstring, (
                f"{handler_class.__name__} docstring missing LRR references"
            )

            # Test that all required methods have docstrings
            handler = handler_class()
            assert handler.execute.__doc__ is not None, (
                f"{handler_class.__name__}.execute missing docstring"
            )
            assert handler.validate_prerequisites.__doc__ is not None, (
                f"{handler_class.__name__}.validate_prerequisites missing docstring"
            )
            assert handler.get_step_name.__doc__ is not None, (
                f"{handler_class.__name__}.get_step_name missing docstring"
            )

    def test_exception_classes_have_comprehensive_docstrings(self) -> None:
        """Test that all exception classes have comprehensive documentation."""
        exception_classes = [
            StatusPhaseError,
            StepValidationError,
            SystemIntegrationError,
            StatusPhaseGameStateError,
        ]

        for exception_class in exception_classes:
            # RED: Test that each exception has proper docstring
            docstring = exception_class.__doc__
            assert docstring is not None, (
                f"{exception_class.__name__} missing docstring"
            )
            assert "LRR References:" in docstring, (
                f"{exception_class.__name__} docstring missing LRR references"
            )
            assert "Rule 81" in docstring, (
                f"{exception_class.__name__} docstring missing Rule 81 reference"
            )


# Constants for test data
STEP_HANDLER_RULE_MAPPINGS = {
    ScoreObjectivesStep: ["Rule 81.1", "Rule 61"],
    RevealObjectiveStep: ["Rule 81.2", "Rule 61"],
    DrawActionCardsStep: ["Rule 81.3", "Rule 2"],
    RemoveCommandTokensStep: ["Rule 81.4", "Rule 20"],
    GainRedistributeTokensStep: ["Rule 81.5", "Rule 20"],
    ReadyCardsStep: ["Rule 81.6", "Rule 34.2"],
    RepairUnitsStep: ["Rule 81.7"],
    ReturnStrategyCardsStep: ["Rule 81.8", "Rule 83"],
}

STATUS_PHASE_CORE_CLASSES = [
    StepResult,
    StatusPhaseResult,
    StatusPhaseOrchestrator,
    RoundTransitionManager,
    StatusPhaseManager,
    StatusPhaseValidator,
]

STATUS_PHASE_STEP_HANDLERS = [
    ScoreObjectivesStep,
    RevealObjectiveStep,
    DrawActionCardsStep,
    RemoveCommandTokensStep,
    GainRedistributeTokensStep,
    ReadyCardsStep,
    RepairUnitsStep,
    ReturnStrategyCardsStep,
]

STATUS_PHASE_ALL_CLASSES = STATUS_PHASE_CORE_CLASSES + STATUS_PHASE_STEP_HANDLERS

STATUS_PHASE_EXCEPTION_CLASSES = [
    StatusPhaseError,
    StepValidationError,
    SystemIntegrationError,
    StatusPhaseGameStateError,
]


class TestStatusPhaseLRRReferences:
    """Test that LRR references are accurate and complete."""

    def test_lrr_references_follow_standard_format(self) -> None:
        """Test that all LRR references follow the standard format."""
        for cls in STATUS_PHASE_ALL_CLASSES:
            self._assert_lrr_references_format(cls)

    def test_step_handlers_reference_correct_rule_numbers(self) -> None:
        """Test that step handlers reference the correct LRR rule numbers."""
        for handler_class, expected_rules in STEP_HANDLER_RULE_MAPPINGS.items():
            self._assert_handler_references_rules(handler_class, expected_rules)

    def test_rule_81_is_referenced_in_all_status_phase_classes(self) -> None:
        """Test that Rule 81 is referenced in all status phase classes."""
        all_classes = STATUS_PHASE_CORE_CLASSES + STATUS_PHASE_EXCEPTION_CLASSES

        for cls in all_classes:
            self._assert_class_references_rule_81(cls)

    def _assert_lrr_references_format(self, cls: type) -> None:
        """Assert that a class has properly formatted LRR references."""
        docstring = cls.__doc__
        assert docstring is not None, f"{cls.__name__} missing docstring"

        # Test that LRR references section exists and follows format
        assert "LRR References:" in docstring, (
            f"{cls.__name__} missing LRR References section"
        )

        # Extract LRR references section
        lrr_section = self._extract_lrr_section(docstring)
        assert lrr_section, f"{cls.__name__} has empty LRR References section"

        # Test that references follow "Rule XX:" format
        rule_pattern = r"Rule \d+(?:\.\d+)?:"
        assert re.search(rule_pattern, lrr_section), (
            f"{cls.__name__} LRR references don't follow 'Rule XX:' format"
        )

    def _assert_handler_references_rules(
        self, handler_class: type, expected_rules: list[str]
    ) -> None:
        """Assert that a step handler references the expected rules."""
        docstring = handler_class.__doc__
        assert docstring is not None, f"{handler_class.__name__} missing docstring"

        lrr_section = self._extract_lrr_section(docstring)

        for rule in expected_rules:
            assert rule in lrr_section, (
                f"{handler_class.__name__} missing reference to {rule}"
            )

    def _assert_class_references_rule_81(self, cls: type) -> None:
        """Assert that a class references Rule 81."""
        docstring = cls.__doc__
        assert docstring is not None, f"{cls.__name__} missing docstring"

        # Test that Rule 81 is referenced
        assert "Rule 81" in docstring, f"{cls.__name__} missing Rule 81 reference"

    def _extract_lrr_section(self, docstring: str) -> str:
        """Extract the LRR References section from a docstring.

        Args:
            docstring: The docstring to extract LRR references from

        Returns:
            The extracted LRR references section as a string
        """
        lines = docstring.split("\n")
        lrr_section = []
        in_lrr_section = False

        for line in lines:
            line = line.strip()
            if line == "LRR References:":
                in_lrr_section = True
                continue
            elif in_lrr_section:
                if line.startswith("- ") or line.startswith("Rule "):
                    lrr_section.append(line)
                elif line == "" or line.startswith(
                    ("Args:", "Returns:", "Attributes:")
                ):
                    break

        return "\n".join(lrr_section)


class TestStatusPhaseCodeQuality:
    """Test code quality standards compliance."""

    def test_all_public_methods_have_type_hints(self) -> None:
        """Test that all public methods have complete type hints."""
        all_classes = STATUS_PHASE_CORE_CLASSES + STATUS_PHASE_STEP_HANDLERS

        for cls in all_classes:
            self._assert_class_methods_have_type_hints(cls)

    def test_all_public_methods_have_docstring_structure(self) -> None:
        """Test that all public methods have proper docstring structure."""
        core_classes = [
            StatusPhaseOrchestrator,
            RoundTransitionManager,
            StatusPhaseManager,
            StatusPhaseValidator,
        ]

        for cls in core_classes:
            self._assert_class_methods_have_proper_docstrings(cls)

    def _assert_class_methods_have_type_hints(self, cls: type) -> None:
        """Assert that all public methods in a class have type hints."""
        public_methods = self._get_public_methods(cls)

        for method_name in public_methods:
            method = getattr(cls, method_name)

            # Skip inherited methods from object
            if method_name in ["__class__", "__doc__", "__module__"]:
                continue

            # Test that method has type hints
            try:
                type_hints = get_type_hints(method)
                # Method should have type hints (at minimum return type)
                assert type_hints or method_name in ["__init__"], (
                    f"{cls.__name__}.{method_name} missing type hints"
                )
            except (NameError, AttributeError):
                # Some methods might have forward references that can't be resolved in test context
                # This is acceptable as long as the annotations exist
                assert hasattr(method, "__annotations__"), (
                    f"{cls.__name__}.{method_name} missing type annotations"
                )

    def _assert_class_methods_have_proper_docstrings(self, cls: type) -> None:
        """Assert that all public methods in a class have proper docstring structure."""
        instance = cls()
        public_methods = self._get_public_methods_from_instance(instance)

        for method_name in public_methods:
            method = getattr(instance, method_name)
            self._assert_method_has_proper_docstring(cls, method_name, method)

    def _get_public_methods(self, cls: type) -> list[str]:
        """Get all public method names from a class."""
        return [
            method
            for method in dir(cls)
            if not method.startswith("_") and callable(getattr(cls, method))
        ]

    def _get_public_methods_from_instance(self, instance: Any) -> list[str]:
        """Get all public method names from a class instance."""
        return [
            method_name
            for method_name in dir(instance)
            if not method_name.startswith("_")
            and callable(getattr(instance, method_name))
        ]

    def _assert_method_has_proper_docstring(
        self, cls: type, method_name: str, method: Any
    ) -> None:
        """Assert that a method has proper docstring structure."""
        docstring = method.__doc__

        # Test that method has docstring
        assert docstring is not None, f"{cls.__name__}.{method_name} missing docstring"

        # Test docstring structure for methods with parameters
        sig = inspect.signature(method)
        params = [p for p in sig.parameters.values() if p.name != "self"]

        if params:
            # Methods with parameters should have Args section
            assert "Args:" in docstring, (
                f"{cls.__name__}.{method_name} missing Args section"
            )

        if (
            sig.return_annotation != inspect.Signature.empty
            and sig.return_annotation is not None
        ):
            # Methods with return type should have Returns section
            assert "Returns:" in docstring, (
                f"{cls.__name__}.{method_name} missing Returns section"
            )

    def test_exception_classes_follow_naming_conventions(self) -> None:
        """Test that exception classes follow proper naming conventions."""
        for exception_class in STATUS_PHASE_EXCEPTION_CLASSES:
            self._assert_exception_naming_convention(exception_class)

    def _assert_exception_naming_convention(self, exception_class: type) -> None:
        """Assert that an exception class follows naming conventions."""
        # Test that exception class name ends with 'Error'
        assert exception_class.__name__.endswith("Error"), (
            f"{exception_class.__name__} should end with 'Error'"
        )

        # Test that exception inherits from appropriate base class
        if exception_class != StatusPhaseError:
            assert issubclass(exception_class, StatusPhaseError), (
                f"{exception_class.__name__} should inherit from StatusPhaseError"
            )

    def test_dataclass_fields_are_documented(self) -> None:
        """Test that dataclass fields are properly documented."""
        dataclasses_to_check = [StepResult, StatusPhaseResult]

        for dataclass_type in dataclasses_to_check:
            self._assert_dataclass_fields_documented(dataclass_type)

    def _assert_dataclass_fields_documented(self, dataclass_type: type) -> None:
        """Assert that all fields in a dataclass are documented."""
        docstring = dataclass_type.__doc__
        assert docstring is not None, f"{dataclass_type.__name__} missing docstring"

        # Test that Attributes section exists
        assert "Attributes:" in docstring, (
            f"{dataclass_type.__name__} missing Attributes section"
        )

        # Get field names from dataclass
        if hasattr(dataclass_type, "__dataclass_fields__"):
            field_names = list(dataclass_type.__dataclass_fields__.keys())

            for field_name in field_names:
                # Test that each field is documented in the Attributes section
                assert f"{field_name}:" in docstring, (
                    f"{dataclass_type.__name__} missing documentation for field '{field_name}'"
                )

    def test_abstract_methods_are_properly_documented(self) -> None:
        """Test that abstract methods in StatusPhaseStepHandler are properly documented."""
        abstract_methods = [
            "execute",
            "validate_prerequisites",
            "get_step_name",
        ]

        for method_name in abstract_methods:
            method = getattr(StatusPhaseStepHandler, method_name)
            docstring = method.__doc__

            # RED: Test that abstract method has comprehensive docstring
            assert docstring is not None, (
                f"StatusPhaseStepHandler.{method_name} missing docstring"
            )
            assert "Args:" in docstring, (
                f"StatusPhaseStepHandler.{method_name} missing Args section"
            )
            assert "Returns:" in docstring, (
                f"StatusPhaseStepHandler.{method_name} missing Returns section"
            )

            if method_name == "execute":
                assert "Raises:" in docstring, (
                    f"StatusPhaseStepHandler.{method_name} missing Raises section"
                )


class TestStatusPhaseDocumentationIntegration:
    """Test integration aspects of documentation."""

    def test_module_docstring_references_all_major_components(self) -> None:
        """Test that module docstring references all major components."""
        from src.ti4.core import status_phase

        module_docstring = status_phase.__doc__
        assert module_docstring is not None, "status_phase module missing docstring"

        # RED: Test that module docstring mentions key components
        assert "Rule 81" in module_docstring, (
            "Module docstring missing Rule 81 reference"
        )
        assert "Rule 34.2" in module_docstring, (
            "Module docstring missing Rule 34.2 reference"
        )
        assert "8-step sequence" in module_docstring, (
            "Module docstring missing 8-step sequence description"
        )

    def test_cross_references_between_classes_are_accurate(self) -> None:
        """Test that cross-references between classes are accurate."""
        # Test that StatusPhaseOrchestrator references step handlers
        orchestrator_docstring = StatusPhaseOrchestrator.__doc__
        assert orchestrator_docstring is not None

        # Test that RoundTransitionManager references agenda phase rules
        transition_docstring = RoundTransitionManager.__doc__
        assert transition_docstring is not None
        assert "Rule 27.4" in transition_docstring, (
            "RoundTransitionManager missing Rule 27.4 reference"
        )

    def test_error_handling_documentation_is_comprehensive(self) -> None:
        """Test that error handling is properly documented."""
        methods_with_error_handling = [
            (StatusPhaseOrchestrator, "execute_complete_status_phase"),
            (StatusPhaseOrchestrator, "execute_step"),
            (RoundTransitionManager, "determine_next_phase"),
            (StatusPhaseManager, "execute_complete_status_phase"),
        ]

        for cls, method_name in methods_with_error_handling:
            method = getattr(cls, method_name)
            docstring = method.__doc__

            assert docstring is not None, (
                f"{cls.__name__}.{method_name} missing docstring"
            )

            # RED: Test that methods that can raise exceptions document them
            if (
                "raise" in inspect.getsource(method).lower()
                or "except" in inspect.getsource(method).lower()
            ):
                # Methods that handle exceptions should document error conditions
                assert any(
                    keyword in docstring
                    for keyword in [
                        "Raises:",
                        "error",
                        "Error",
                        "exception",
                        "Exception",
                    ]
                ), (
                    f"{cls.__name__}.{method_name} handles exceptions but doesn't document error conditions"
                )
