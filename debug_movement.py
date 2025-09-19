#!/usr/bin/env python3

from src.ti4.core.galaxy import Galaxy
from src.ti4.core.movement import MovementValidator, MovementOperation
from src.ti4.core.system import System
from src.ti4.core.unit import Unit, UnitType
from src.ti4.core.hex_coordinate import HexCoordinate

def debug_movement():
    """Debug the movement validation issue."""
    galaxy = Galaxy()
    validator = MovementValidator(galaxy)
    
    # Create systems that are 2 hexes apart
    coord_a = HexCoordinate(0, 0)
    coord_c = HexCoordinate(2, 0)  # 2 hexes away
    system_a = System("system_a")
    system_c = System("system_c")
    
    galaxy.place_system(coord_a, "system_a")
    galaxy.place_system(coord_c, "system_c")
    galaxy.register_system(system_a)
    galaxy.register_system(system_c)
    
    # Create unit with Gravity Drive (movement 2)
    unit = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Movement 1
    unit.add_technology("gravity_drive")  # Increases movement to 2
    system_a.place_unit_in_space(unit)
    
    print(f"Unit base movement: {unit.get_movement()}")
    print(f"Distance between systems: {coord_a.distance_to(coord_c)}")
    
    # Test movement should be valid with technology
    movement = MovementOperation(
        unit=unit,
        from_system_id="system_a",
        to_system_id="system_c",
        player_id="player1",
        player_technologies={"gravity_drive"},
    )
    
    # Debug the validation steps
    from_system = galaxy.get_system("system_a")
    to_system = galaxy.get_system("system_c")
    print(f"From system exists: {from_system is not None}")
    print(f"To system exists: {to_system is not None}")
    
    if from_system:
        print(f"From system has command token: {from_system.has_command_token('player1')}")
    
    path = galaxy.find_path("system_a", "system_c")
    print(f"Path found: {path}")
    
    print(f"TI4 rules validation: {validator._validate_ti4_movement_rules(movement)}")
    
    # Check the cached validation
    tech_key = frozenset(movement.player_technologies) if movement.player_technologies else frozenset()
    cached_result = validator._is_valid_movement_cached(
        UnitType(movement.unit.unit_type),
        movement.from_system_id,
        movement.to_system_id,
        tech_key,
    )
    print(f"Cached validation result: {cached_result}")
    
    # Check the rule engine directly
    from_coord = galaxy.get_system_coordinate("system_a")
    to_coord = galaxy.get_system_coordinate("system_c")
    
    if from_coord and to_coord:
        from src.ti4.core.movement_rules import MovementContext
        mock_unit = Unit(unit_type=UnitType.CARRIER, owner="temp")
        context = MovementContext(
            unit=mock_unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies={"gravity_drive"},
            galaxy=galaxy,
        )
        
        rule_engine_result = validator._rule_engine.can_move(context)
        print(f"Rule engine result: {rule_engine_result}")
        
        # Check individual rules
        for i, rule in enumerate(validator._rule_engine.rules):
            rule_result = rule.can_move(context)
            movement_range = rule.get_movement_range(mock_unit, {"gravity_drive"})
            print(f"Rule {i} ({type(rule).__name__}): can_move={rule_result}, movement_range={movement_range}")
    
    final_result = validator.validate_movement(movement)
    print(f"Final validation result: {final_result}")

if __name__ == "__main__":
    debug_movement()