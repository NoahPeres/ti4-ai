# Implementation Plan

- [x] 1. Fix duplicate transaction ID validation in GameState
  - Add validation check in add_pending_transaction method
  - Raise ValueError with descriptive message including transaction ID
  - Write tests to verify duplicate prevention and error message content
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement atomic transaction operations
  - Reorder apply_transaction_effects to apply effects before history commit
  - Apply resource effects first, then promissory note effects, then validate
  - Only commit to history after successful effects and validation
  - Write tests to verify atomicity and rollback on failure
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 3. Fix immutability violations in resource effects
  - Add import copy to game_state.py
  - Use copy.deepcopy for Player objects before mutation in _apply_resource_effects
  - Update all player mutation points to work on copies
  - Write tests to verify immutability with identity checks
  - _Requirements: 3.1, 3.4_

- [x] 4. Fix PromissoryNoteManager cloning in promissory effects
  - Implement proper cloning that preserves both player hands and available notes
  - Copy _player_hands dictionary and _available_notes set
  - Update _apply_promissory_note_effects to use proper cloning
  - Write tests to verify complete state preservation
  - _Requirements: 3.2, 3.3, 3.4_

- [x] 5. Implement zero-amount transfer handling in ResourceManager
  - Add early return for amount == 0 in transfer_trade_goods
  - Add early return for amount == 0 in transfer_commodities
  - Update _validate_transfer_inputs to allow zero (change <= 0 to < 0)
  - Write tests to verify no-op behavior for zero amounts
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 6. Synchronize transaction manager with GameState on propose
  - Update propose_transaction to call GameState.add_pending_transaction
  - Add hasattr check for backward compatibility
  - Update manager's _game_state reference after GameState update
  - Write tests to verify synchronization between manager cache and GameState
  - _Requirements: 5.1_

- [x] 7. Use GameState for transaction execution in accept path
  - Replace direct ResourceManager calls with GameState.apply_transaction_effects
  - Build completed transaction before calling GameState method
  - Update manager cache after successful GameState execution
  - Write tests to verify delegation to GameState methods
  - _Requirements: 5.2_

- [x] 8. Synchronize GameState on reject and cancel operations
  - Update reject_transaction to remove from GameState.pending_transactions
  - Update cancel_transaction to remove from GameState.pending_transactions
  - Use safe removal with copy() and pop() with default
  - Write tests to verify removal from both manager cache and GameState
  - _Requirements: 5.3, 5.4_

- [x] 9. Implement robust observer notification pattern
  - Wrap each observer call in try-catch block in _notify_transaction_observers
  - Continue with remaining observers if one fails
  - Add TODO comment for project logger integration
  - Write tests to verify resilience to observer failures
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 10. Update tests to use specific exception types
  - Replace pytest.raises(Exception) with pytest.raises(TransactionValidationError)
  - Add imports for specific exception types in test files
  - Update test_rule_28_error_handling.py validation tests
  - Verify all exception assertions use specific types
  - _Requirements: 6.1, 7.4_

- [x] 11. Improve rollback handling to preserve asset types
  - Document the commodity rollback issue in TransactionRollbackError
  - Add context information to rollback errors (asset_type, amounts)
  - Update rollback logic to track original asset types
  - Write tests to verify proper asset type preservation in rollback
  - _Requirements: 6.2, 6.4_

- [x] 12. Enhance test quality and remove implementation coupling
  - Remove assertions on private attributes (_galaxy, _game_state, etc.)
  - Add identity checks (assert new_state is not old_state) for immutability
  - Assert explicit success/failure states in transaction results
  - Add specific error message content assertions
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 13. Remove unused parameters and improve method signatures
  - Remove unused receiving_player parameter from _apply_transaction_offer
  - Update all call sites to match new signature
  - Add proper type hints instead of Any where possible
  - Document ValueError conditions in method docstrings
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 14. Add GameState access to TransactionAPI
  - Add get_game_state() method to TransactionAPI
  - Include GameState reference in TransactionAPIResult if needed
  - Update API documentation to describe state access
  - Write tests to verify API provides access to updated GameState
  - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [x] 15. Consolidate duplicate transaction history logic
  - Remove duplicate TransactionHistoryManager if it exists
  - Delegate all history operations to GameState methods
  - Update any direct history access to use GameState as source of truth
  - Write tests to verify single source of truth for transaction history
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 16. Run comprehensive validation and testing
  - Execute full test suite to ensure no regressions
  - Run type checking with strict settings
  - Verify all quality gates pass
  - Update any remaining tests that fail due to changes
  - _Requirements: All requirements validation_
