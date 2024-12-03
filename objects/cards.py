from cost import Mana_Cost
from objects.abilities import *
from card import Artifact_Card, Creature_Card, Enchantment_Card, Instant_Card, Land_Card, Sorcery_Card
from enums import BasicLandType, CardType, CreatureType, ManaCost, SuperType

# TODO: Tie the basic land abilities to the basic land types.
plains = Land_Card("Plains", [SuperType.BASIC, CardType.LAND, BasicLandType.PLAINS], [plains_ability])
island = Land_Card("Island", [SuperType.BASIC, CardType.LAND, BasicLandType.ISLAND], [island_ability])
swamp = Land_Card("Swamp ", [SuperType.BASIC, CardType.LAND, BasicLandType.SWAMP], [swamp_ability])
mountain = Land_Card("Mountn", [SuperType.BASIC, CardType.LAND, BasicLandType.MOUNTAIN], [mountain_ability])
forest = Land_Card("Forest", [SuperType.BASIC, CardType.LAND, BasicLandType.FOREST], [forest_ability])
everywhere = Land_Card("Everywhere", [CardType.LAND, BasicLandType.PLAINS, BasicLandType.ISLAND, BasicLandType.SWAMP, BasicLandType.MOUNTAIN, BasicLandType.FOREST], [plains_ability,
                       island_ability, swamp_ability, mountain_ability, forest_ability])

# savannah_lions = Creature_Card("Savannah Lions", [ManaCost.WHITE], [CardType.CREATURE], [], 2, 1)
# triton_shorethief = Creature_Card("Triton Shorethief", [ManaCost.BLUE], [CardType.CREATURE], [], 1, 2)
# dwarven_trader = Creature_Card("Dwarven Trader", [ManaCost.RED], [CardType.CREATURE], [], 1, 1)
# woodland_druid = Creature_Card("Woodland Druid", [ManaCost.GREEN], [CardType.CREATURE], [], 1, 2)

human = Creature_Card("Human", "W", [CardType.CREATURE], [], 1, 1)
merfolk = Creature_Card("Merfolk", "U", [CardType.CREATURE], [], 1, 1)
goblin = Creature_Card("Goblin", "R",  [CardType.CREATURE], [], 1, 1)
druid = Creature_Card("Druid", "G",  [CardType.CREATURE], [], 1, 1)

ox = Creature_Card("Ox", "1W", [CardType.CREATURE], [], 2, 2)
crab = Creature_Card("Crab", "1U", [CardType.CREATURE], [], 1, 3)
dwarf = Creature_Card("Dwarf", "1R", [CardType.CREATURE], [], 3, 1)
bear = Creature_Card("Bear", "1G", [CardType.CREATURE], [], 2, 2)

horse = Creature_Card("Horse", "2W", [CardType.CREATURE], [], 3, 3)
serpent = Creature_Card("Serpent", "2U", [CardType.CREATURE], [], 2, 5)
drake = Creature_Card("Drake", "2R", [CardType.CREATURE], [], 4, 2)
ent = Creature_Card("Ent", "2G", [CardType.CREATURE], [], 3, 3)

angel = Creature_Card("Angel", "3W", [CardType.CREATURE], [], 4, 4)
sphinx = Creature_Card("Sphinx", "3U", [CardType.CREATURE], [], 3, 6)
dragon = Creature_Card("Dragon", "3R", [CardType.CREATURE], [], 7, 1)
dinosaur = Creature_Card("Dinosaur", "3G", [CardType.CREATURE], [], 5, 5)

# lightning_bolt = Instant_Card("Lightning Bolt", [ManaCost.RED], [CardType.INSTANT], [lightning_ability])
# rals_reinforcements = Sorcery_Card("Ral's Reinforcements", [ManaCost.GENERIC, ManaCost.RED], [
#                                    CardType.SORCERY], [reinforcements_ability])

destroy = Sorcery_Card("Destroy", "1", [CardType.SORCERY], [destroy_ability])
draw = Instant_Card("Draw", "1", [CardType.INSTANT], [draw_card_ability])


aegis_turtle = Creature_Card("Aegis Turtle", "U", [CardType.CREATURE, CreatureType.TURTLE], [], 0, 5)
ambush_wolf = Creature_Card("Ambush Wolf", "2G", [CardType.CREATURE, CreatureType.WOLF], [flash, ambush_wolf_etb], 4, 2)
apothecary_stomper = Creature_Card("Apothecary Stomper", "4GG", [CardType.CREATURE, CreatureType.ELEPHANT], [
                                   vigilance, apothecary_stomper_etb], 4, 4)
armasaur_guide = Creature_Card("Armasaur Guide", "4W", [CardType.CREATURE, CreatureType.DINOSAUR], [
                               vigilance, armasaur_guide_attack], 4, 4)
axgard_cavalry = Creature_Card("Axgard Cavalry", "1R", [CardType.CREATURE,
                               CreatureType.DWARF, CreatureType.BERSERKER], [axgard_cavalry_tap], 2, 2)
bake_into_a_pie = Instant_Card("Bake into a Pie", "2BB", [CardType.INSTANT], [bake_into_a_pie_ability])
banishing_light = Enchantment_Card("Banishing Light", "2W", [CardType.ENCHANTMENT], [banishing_light_ability])
beast_kin_ranger = Creature_Card("Beast-Kin Ranger", "2G",
                                 [CardType.CREATURE, CreatureType.ELF, CreatureType.RANGER], [trample, beastkin_ranger_pump], 3, 3)
bigfin_bouncer = Creature_Card("Bigfin Bouncer", "3U", [CardType.CREATURE,
                               CreatureType.SHARK, CreatureType.PIRATE], [bigfin_bouncer_etb], 3, 2)
bite_down = Instant_Card("Bite Down", "1G", [CardType.INSTANT], [bite_down_ability])
bloodfell_caves = Land_Card("Bloodfell Caves", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, rakdos_land_ability])
blossoming_sands = Land_Card("Blossoming Sands", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, selesnya_land_ability])
broken_wings = Instant_Card("Broken Wings", "2G", [CardType.INSTANT], [broken_wings_ability])
burglar_rat = Creature_Card("Burglar Rat", "1B", [CardType.CREATURE, CreatureType.RAT], [burglar_etb], 1, 1)
burst_lightning = Instant_Card("Burst Lightning", "R", [CardType.INSTANT], [burst_lightning_ability, kicker("4")])
bushwhack = Sorcery_Card("Bushwhack", "G", [CardType.SORCERY], [bushwhack_ability])
cackling_prowler = Creature_Card("Cackling Prowler", "3G", [CardType.CREATURE, CreatureType.HYENA, CreatureType.ROGUE], [
                                 ward("2"), cackling_prowler_morbid], 4, 3)
campus_guide = Creature_Card("Campus Guide", "2", [CardType.ARTIFACT, CardType.CREATURE, CreatureType.GOLEM], [campus_guide_etb], 2, 1)
cathar_commando = Creature_Card("Cathar Commando", "1W", [CardType.CREATURE,
                                CreatureType.HUMAN, CreatureType.SOLDIER], [flash, cathar_sac], 3, 1)
courageous_goblin = Creature_Card("Courageous Goblin", "1R", [
                                  CardType.CREATURE, CreatureType.GOBLIN], [courageous_goblin_attack], 2, 2)
crackling_cyclops = Creature_Card("Crackling Cyclops", "2R", [
                                  CardType.CREATURE, CreatureType.CYCLOPS, CreatureType.WIZARD], [crackling_cyclops_pump], 0, 4)
crypt_feaster = Creature_Card("Crypt Feaster", "3B", [CardType.CREATURE, CreatureType.ZOMBIE], [menace, crypt_feaster_threshold], 3, 4)
dazzling_angel = Creature_Card("Dazzling Angel", "2W", [CardType.CREATURE, CreatureType.ANGEL], [flying, dazzling_angel_gain], 2, 3)
dismal_backwater = Land_Card("Dismal Backwater", [CardType.LAND], [enters_tapped_replacement, gain_1_etb, dimir_land_ability])
dwynens_elite = Creature_Card("Dwynen's Elite", "1G", [CardType.CREATURE,
                              CreatureType.ELF, CreatureType.WARRIOR], [dwynens_elite_etb], 2, 2)
eaten_alive = Sorcery_Card("Eaten Alive", "B", [CardType.SORCERY], [eaten_alive_ability, eaten_alive_extra_cost])
elementalist_adept = Creature_Card("Elementalist Adept", "1U", [
                                   CardType.CREATURE, CreatureType.HUMAN, CreatureType.WIZARD], [flash, prowess], 2, 1)
elfsworn_giant = Creature_Card("Elfsworn Giant", "3GG", [CardType.CREATURE, CreatureType.GIANT], [
                               reach, elfsworn_giant_landfall], 5, 3)
erudite_wizard = Creature_Card("Erudite Wizard", "2U", [CardType.CREATURE,
                               CreatureType.HUMAN, CreatureType.WIZARD], [erudite_wizard_2card], 2, 3)
evolving_wilds = Land_Card("Evolving Wilds", [CardType.LAND], [evolving_wilds_sac])
fake_your_own_death = Instant_Card("Fake Your Own Death", "1B", [CardType.INSTANT], [fake_your_own_death_ability])
fanatical_firebrand = Creature_Card("Fanatical Firebrand", "R", [CardType.CREATURE, CreatureType.GOBLIN, CreatureType.PIRATE], [
                                    haste, fanatical_firebrand_sac], 1, 1)
felidar_savior = Creature_Card("Felidar Savior", "3W", [CardType.CREATURE,
                               CreatureType.CAT, CreatureType.BEAST], [lifelink, felidar_savior_etb], 2, 3)
firebrand_archer = Creature_Card("Firebrand Archer", "1R", [
                                 CardType.CREATURE, CreatureType.HUMAN, CreatureType.ARCHER], [firebrand_archer_ping], 2, 1)
fleeting_distraction = Instant_Card("Fleeting Distraction", "U", [CardType.INSTANT], [fleeting_distraction_ability])
fleeting_flight = Instant_Card("Fleeting Flight", "W", [CardType.INSTANT], [fleeting_flight_ability])
giant_growth = Instant_Card("Giant Growth", "G", [CardType.INSTANT], [giant_growth_ability])
gleaming_barrier = Creature_Card("Gleaming Barrier", "2", [CardType.ARTIFACT, CardType.CREATURE, CreatureType.WALL], [
                                 defender, gleaming_barrier_death], 0, 4)
gnarlid_colony = Creature_Card("Gnarlid Colony", "1G", [CardType.CREATURE, CreatureType.BEAST], [
                               kicker("2G"), gnarlid_kicked_enters, gnarlid_counter_lord], 2, 2)
goblin_boarders = Creature_Card("Goblin Boarders", "2R", [CardType.CREATURE,
                                CreatureType.GOBLIN, CreatureType.PIRATE], [goblin_boarders_enters], 3, 2)
goblin_surprise = Instant_Card("Goblin Surprise", "2R", [CardType.INSTANT], [goblin_surprise_ability])
goldvein_pick = Artifact_Card("Goldvein Pick", "2", [CardType.ARTIFACT, ArtifactType.EQUIPMENT], [
                              goldvein_equip_buff, goldvein_damage_trigger, equip("1")])
gorehorn_raider = Creature_Card("Gorehorn Raider", "4R", [CardType.CREATURE,
                                CreatureType.MINOTAUR, CreatureType.PIRATE], [gorehorn_raider_etb], 4, 4)
grow_from_the_ashes = Sorcery_Card("Grow from the Ashes", "2G", [CardType.SORCERY], [grow_from_the_ashes_ability, kicker("2")])
gutless_plunderer = Creature_Card("Gutless Plunderer", "2B", [CardType.CREATURE, CreatureType.SKELETON, CreatureType.PIRATE], [
                                  deathtouch, gutless_plunderer_etb], 2, 2)
hare_apparent = Creature_Card("Hare Apparent", "1W", [CardType.CREATURE,
                              CreatureType.RABBIT, CreatureType.NOBLE], [hare_apparent_etb], 2, 2)
