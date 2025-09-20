# Player Supply System Architecture

## Overview
The transaction system currently lacks validation against player resources. Players should not be able to give more of something than they actually have.

## Current Gap
- `TransactionOffer` allows any values without validation
- No concept of player "supply" or "play area"
- Similar to how `CommandSheet` tracks command tokens, we need resource tracking

## Required Components

### 1. Player Supply/Play Area Class
```python
@dataclass
class PlayerSupply:
    """Tracks a player's available resources for transactions."""

    trade_goods: int = 0
    commodities: int = 0
    promissory_notes: list[PromissoryNote] = field(default_factory=list)
    relic_fragments: int = 0

    def can_afford(self, offer: TransactionOffer) -> bool:
        """Check if player has sufficient resources for the offer."""

    def deduct_resources(self, offer: TransactionOffer) -> "PlayerSupply":
        """Return new supply with resources deducted."""

    def add_resources(self, offer: TransactionOffer) -> "PlayerSupply":
        """Return new supply with resources added."""
```

### 2. Integration Points

#### GameState Integration
- Add `player_supplies: dict[str, PlayerSupply]` to GameState
- Update supplies when transactions occur
- Validate offers against current supplies

#### Transaction Manager Enhancement
```python
def execute_transaction(
    self,
    game_state: GameState,  # Add game state parameter
    player1: str,
    player2: str,
    player1_offer: TransactionOffer,
    player2_offer: TransactionOffer,
) -> tuple[TransactionResult, GameState]:
    """Execute transaction with supply validation."""

    # Validate both players can afford their offers
    if not game_state.get_player_supply(player1).can_afford(player1_offer):
        return TransactionResult(success=False, error="Player1 insufficient resources"), game_state

    # Execute transaction and update supplies
    new_state = game_state.update_player_supplies(...)
    return TransactionResult(success=True, ...), new_state
```

### 3. Resource Sources

#### Trade Goods & Commodities
- Planets produce commodities
- Commodities convert to trade goods when traded
- Strategy cards provide trade goods
- Technology cards may provide resources

#### Promissory Notes
- Each faction starts with specific promissory notes
- Some are gained through gameplay
- Each note can only be held by one player at a time

#### Relic Fragments
- Gained from exploration
- Used to purchase relics
- Limited supply per game

### 4. Validation Rules

#### Transaction Validation
- Player must have >= offered amounts
- Promissory notes must be owned by offering player
- Cannot offer the same promissory note twice

#### Edge Cases
- What happens if resources change between offer and execution?
- Simultaneous transactions in multiplayer
- Resource limits (max commodities based on planets)

## Implementation Priority

### Phase 1: Basic Supply Tracking
- Create PlayerSupply class
- Add to GameState
- Basic validation in TransactionManager

### Phase 2: Resource Integration
- Connect to planet production
- Strategy card effects
- Technology effects

### Phase 3: Advanced Features
- Promissory note ownership tracking
- Resource conversion rules
- Transaction history/audit trail

## Related Systems

### Existing Patterns
- `CommandSheet` for command token tracking
- `GameState` immutable updates
- Validation patterns in existing rules

### Future Integration
- Production system (planets → commodities)
- Strategy card effects
- Technology tree effects
- Faction abilities affecting resources

## LRR References
- Rule 94.3: Lists exchangeable items
- Rule 75: Trade Goods mechanics
- Rule 19: Commodities mechanics
- Rule 80: Promissory Notes mechanics

## Notes
- This is a foundational system that many other rules depend on
- Should be implemented before complex transaction features
- Consider performance implications for frequent resource checks
- Maintain immutability patterns consistent with existing codebase
