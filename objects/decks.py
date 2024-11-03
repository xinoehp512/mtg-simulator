from deck import Deck
import objects.cards as cards


deck1 = Deck([cards.plains] * 8 +
             [cards.island] * 8 +
             [cards.human] * 1 +
             [cards.merfolk] * 1 +
             [cards.ox] * 3 +
             [cards.crab] * 3 +
             [cards.horse] * 2 +
             [cards.serpent] * 2 +
             [cards.angel] +
             [cards.sphinx]
             )
deck2 = Deck([cards.mountain] * 8 +
             [cards.forest] * 8 +
             [cards.goblin] * 1 +
             [cards.druid] * 1 +
             [cards.dwarf] * 3 +
             [cards.bear] * 3 +
             [cards.drake] * 2 +
             [cards.ent] * 2 +
             [cards.dragon] +
             [cards.dinosaur]
             )
deck3 = Deck([cards.mountain]*10 + [cards.lightning_bolt]*20)
deck4 = Deck([cards.forest]*10+[cards.druid]*10+[cards.giant_growth]*10)
deck5 = Deck([cards.mountain]*10+[cards.rals_reinforcements]*10)
