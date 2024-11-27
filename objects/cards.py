from cost import Mana_Cost
from objects.abilities import *
from card import Creature_Card, Enchantment_Card, Instant_Card, Land_Card, Sorcery_Card
from enums import BasicLandType, CardType, CreatureType, ManaCost, SuperType

# TODO: Tie the basic land abilities to the basic land types.
plains = Land_Card("Plains", [SuperType.BASIC, CardType.LAND, BasicLandType.PLAINS], [plains_ability])
island = Land_Card("Island", [SuperType.BASIC, CardType.LAND, BasicLandType.ISLAND], [island_ability])
swamp = Land_Card("Swamp ", [SuperType.BASIC, CardType.LAND, BasicLandType.SWAMP], [swamp_ability])
mountain = Land_Card("Mountn", [SuperType.BASIC, CardType.LAND, BasicLandType.MOUNTAIN], [mountain_ability])
forest = Land_Card("Forest", [SuperType.BASIC, CardType.LAND, BasicLandType.FOREST], [forest_ability])
everywhere = Land_Card("Everywhere", [CardType.LAND, BasicLandType.PLAINS, BasicLandType.ISLAND, BasicLandType.SWAMP, BasicLandType.MOUNTAIN, BasicLandType.FOREST], [plains_ability,
                       island_ability, swamp_ability, mountain_ability, forest_ability])

# savannah_lions = Creature_Card("Savannah Lions (W)", [ManaCost.WHITE], [CardType.CREATURE], [], 2, 1)
# triton_shorethief = Creature_Card("Triton Shorethief (U)", [ManaCost.BLUE], [CardType.CREATURE], [], 1, 2)
# dwarven_trader = Creature_Card("Dwarven Trader (R)", [ManaCost.RED], [CardType.CREATURE], [], 1, 1)
# woodland_druid = Creature_Card("Woodland Druid (G)", [ManaCost.GREEN], [CardType.CREATURE], [], 1, 2)

human = Creature_Card("Human (W)", Mana_Cost.from_string("W"), [CardType.CREATURE], [], 1, 1)
merfolk = Creature_Card("Merfolk (U)", Mana_Cost.from_string("U"), [CardType.CREATURE], [], 1, 1)
goblin = Creature_Card("Goblin (R)", Mana_Cost.from_string("R"),  [CardType.CREATURE], [], 1, 1)
druid = Creature_Card("Druid (G)", Mana_Cost.from_string("G"),  [CardType.CREATURE], [], 1, 1)

ox = Creature_Card("Ox (1W)", Mana_Cost.from_string("1W"), [CardType.CREATURE], [], 2, 2)
crab = Creature_Card("Crab (1U)", Mana_Cost.from_string("1U"), [CardType.CREATURE], [], 1, 3)
dwarf = Creature_Card("Dwarf (1R)", Mana_Cost.from_string("1R"), [CardType.CREATURE], [], 3, 1)
bear = Creature_Card("Bear (1G)", Mana_Cost.from_string("1G"), [CardType.CREATURE], [], 2, 2)

horse = Creature_Card("Horse (2W)", Mana_Cost.from_string("2W"), [CardType.CREATURE], [], 3, 3)
serpent = Creature_Card("Serpent (2U)", Mana_Cost.from_string("2U"), [CardType.CREATURE], [], 2, 5)
drake = Creature_Card("Drake (2R)", Mana_Cost.from_string("2R"), [CardType.CREATURE], [], 4, 2)
ent = Creature_Card("Ent (2G)", Mana_Cost.from_string("2G"), [CardType.CREATURE], [], 3, 3)

angel = Creature_Card("Angel (3W)", Mana_Cost.from_string("3W"), [CardType.CREATURE], [], 4, 4)
sphinx = Creature_Card("Sphinx (3U)", Mana_Cost.from_string("3U"), [CardType.CREATURE], [], 3, 6)
dragon = Creature_Card("Dragon (3R)", Mana_Cost.from_string("3R"), [CardType.CREATURE], [], 7, 1)
dinosaur = Creature_Card("Dinosaur (3G)", Mana_Cost.from_string("3G"), [CardType.CREATURE], [], 5, 5)

# lightning_bolt = Instant_Card("Lightning Bolt (R)", [ManaCost.RED], [CardType.INSTANT], [lightning_ability])
# giant_growth = Instant_Card("Giant Growth (G)", [ManaCost.GREEN], [CardType.INSTANT], [giant_growth_ability])
# rals_reinforcements = Sorcery_Card("Ral's Reinforcements (1R)", [ManaCost.GENERIC, ManaCost.RED], [
#                                    CardType.SORCERY], [reinforcements_ability])

destroy = Sorcery_Card("Destroy (1)", Mana_Cost.from_string("1"), [CardType.SORCERY], [destroy_ability])
draw = Instant_Card("Draw (1)", Mana_Cost.from_string("1"), [CardType.INSTANT], [draw_card_ability])


aegis_turtle = Creature_Card("Aegis Turtle (U)", Mana_Cost.from_string("U"), [CardType.CREATURE, CreatureType.TURTLE], [], 0, 5)
ambush_wolf = Creature_Card("Ambush Wolf (2G)", Mana_Cost.from_string(
    "2G"), [CardType.CREATURE, CreatureType.WOLF], [flash, ambush_wolf_etb], 4, 2)
apothecary_stomper = Creature_Card("Apothecary Stomper (4GG)", Mana_Cost.from_string(
    "4GG"), [CardType.CREATURE, CreatureType.ELEPHANT], [vigilance, apothecary_stomper_etb], 4, 4)
armasaur_guide = Creature_Card("Armasaur Guide (4W)", Mana_Cost.from_string(
    "4W"), [CardType.CREATURE, CreatureType.DINOSAUR], [vigilance, armasaur_guide_attack], 4, 4)
axgard_cavalry = Creature_Card("Axgard Cavalry (1R)", Mana_Cost.from_string(
    "1R"), [CardType.CREATURE, CreatureType.DWARF, CreatureType.BERSERKER], [axgard_cavalry_tap], 2, 2)
bake_into_a_pie = Instant_Card("Bake into a Pie (2BB)", Mana_Cost.from_string("2BB"), [CardType.INSTANT], [bake_into_a_pie_ability])
banishing_light = Enchantment_Card("Banishing Light (2W)", Mana_Cost.from_string("2W"),
                                   [CardType.ENCHANTMENT], [banishing_light_ability])
beast_kin_ranger = Creature_Card("Beast-Kin Ranger (2G)", Mana_Cost.from_string("2G"),
                                 [CardType.CREATURE, CreatureType.ELF, CreatureType.RANGER], [trample, beastkin_ranger_pump], 3, 3)
bigfin_bouncer = Creature_Card("Bigfin Bouncer (3U)", Mana_Cost.from_string(
    "3U"), [CardType.CREATURE, CreatureType.SHARK, CreatureType.PIRATE], [bigfin_bouncer_etb], 3, 2)
bite_down = Instant_Card("Bite Down (1G)", Mana_Cost.from_string("1G"), [CardType.INSTANT], [bite_down_ability])
bloodfell_caves = Land_Card("Bloodfell Caves", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, rakdos_land_ability])
blossoming_sands = Land_Card("Blossoming Sands", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, selesnya_land_ability])
broken_wings = Instant_Card("Broken Wings (2G)", Mana_Cost.from_string("2G"), [CardType.INSTANT], [broken_wings_ability])
burglar_rat = Creature_Card("Burglar Rat (1B)", Mana_Cost.from_string(
    "1B"), [CardType.CREATURE, CreatureType.RAT], [burglar_etb], 1, 1)
burst_lightning = Instant_Card("Burst Lightning (R)", Mana_Cost.from_string("R"), [CardType.INSTANT], [
    burst_lightning_ability, kicker(Total_Cost([Mana_Cost.from_string("4")], type=AdditionalCostType.KICKED))])
bushwhack = Sorcery_Card("Bushwhack (G)", Mana_Cost.from_string("G"), [CardType.SORCERY], [bushwhack_ability])
cackling_prowler = Creature_Card("Cackling Prowler (3G)", Mana_Cost.from_string(
    "3G"), [CardType.CREATURE, CreatureType.HYENA, CreatureType.ROGUE], [ward(Total_Cost([Mana_Cost.from_string("2")])), cackling_prowler_morbid], 4, 3)
campus_guide = Creature_Card("Campus Guide (2)", Mana_Cost.from_string(
    "2"), [CardType.ARTIFACT, CardType.CREATURE, CreatureType.GOLEM], [campus_guide_etb], 2, 1)
cathar_commando = Creature_Card("Cathar Commando (1W)", Mana_Cost.from_string(
    "1W"), [CardType.CREATURE, CreatureType.HUMAN, CreatureType.SOLDIER], [flash, cathar_sac], 3, 1)
courageous_goblin = Creature_Card("Courageous Goblin (1R)", Mana_Cost.from_string(
    "1R"), [CardType.CREATURE, CreatureType.GOBLIN], [courageous_goblin_attack], 2, 2)
crackling_cyclops = Creature_Card("Crackling Cyclops (2R)", Mana_Cost.from_string(
    "2R"), [CardType.CREATURE, CreatureType.CYCLOPS, CreatureType.WIZARD], [crackling_cyclops_pump], 0, 4)
crypt_feaster = Creature_Card("Crypt Feaster (3B)", Mana_Cost.from_string(
    "3B"), [CardType.CREATURE, CreatureType.ZOMBIE], [menace, crypt_feaster_threshold], 3, 4)
dazzling_angel = Creature_Card("Dazzling Angel (2W)", Mana_Cost.from_string(
    "2W"), [CardType.CREATURE, CreatureType.ANGEL], [flying, dazzling_angel_gain], 2, 3)
dismal_backwater = Land_Card("Dismal Backwater", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, dimir_land_ability])
dwynens_elite = Creature_Card("Dwynen's Elite (1G)", Mana_Cost.from_string(
    "1G"), [CardType.CREATURE, CreatureType.ELF, CreatureType.WARRIOR], [dwynens_elite_etb], 2, 2)
eaten_alive = Sorcery_Card("Eaten Alive (B)", Mana_Cost.from_string(
    "B"), [CardType.SORCERY], [eaten_alive_ability, eaten_alive_extra_cost])
elementalist_adept = Creature_Card("Elementalist Adept (1U)", Mana_Cost.from_string(
    "1U"), [CardType.CREATURE, CreatureType.HUMAN, CreatureType.WIZARD], [flash, prowess], 2, 1)
elfsworn_giant = Creature_Card("Elfsworn Giant (3GG)", Mana_Cost.from_string(
    "3GG"), [CardType.CREATURE, CreatureType.GIANT], [reach, elfsworn_giant_landfall], 5, 3)
erudite_wizard = Creature_Card("Erudite Wizard (2U)", Mana_Cost.from_string(
    "2U"), [CardType.CREATURE, CreatureType.HUMAN, CreatureType.WIZARD], [erudite_wizard_2card], 2, 3)
evolving_wilds = Land_Card("Evolving Wilds", [CardType.LAND], [evolving_wilds_sac])
fake_your_own_death = Instant_Card("Fake Your Own Death (1B)", Mana_Cost.from_string("1B"),
                                   [CardType.INSTANT], [fake_your_own_death_ability])
