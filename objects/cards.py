from cost import Mana_Cost
from objects.abilities import *
from card import Card
from enums import BasicLandType, CardType, CreatureType, ManaCost, SuperType

# TODO: Tie the basic land abilities to the basic land types.
plains = Card("Plains", None, [SuperType.BASIC, CardType.LAND, BasicLandType.PLAINS], [plains_ability])
island = Card("Island", None, [SuperType.BASIC, CardType.LAND, BasicLandType.ISLAND], [island_ability])
swamp = Card("Swamp", None, [SuperType.BASIC, CardType.LAND, BasicLandType.SWAMP], [swamp_ability])
mountain = Card("Mountn", None, [SuperType.BASIC, CardType.LAND, BasicLandType.MOUNTAIN], [mountain_ability])
forest = Card("Forest", None, [SuperType.BASIC, CardType.LAND, BasicLandType.FOREST], [forest_ability])
everywhere = Card("Everywhere", None, [CardType.LAND, BasicLandType.PLAINS, BasicLandType.ISLAND, BasicLandType.SWAMP,
                  BasicLandType.MOUNTAIN, BasicLandType.FOREST], [plains_ability, island_ability, swamp_ability, mountain_ability, forest_ability])

# savannah_lions = Card("Savannah Lions", [ManaCost.WHITE], [CardType.CREATURE], [], 2, 1)
# triton_shorethief = Card("Triton Shorethief", [ManaCost.BLUE], [CardType.CREATURE], [], 1, 2)
# dwarven_trader = Card("Dwarven Trader", [ManaCost.RED], [CardType.CREATURE], [], 1, 1)
# woodland_druid = Card("Woodland Druid", [ManaCost.GREEN], [CardType.CREATURE], [], 1, 2)

human = Card("Human", "W", [CardType.CREATURE], [], power=1, toughness=1)
merfolk = Card("Merfolk", "U", [CardType.CREATURE], [], power=1, toughness=1)
goblin = Card("Goblin", "R", [CardType.CREATURE], [], power=1, toughness=1)
druid = Card("Druid", "G", [CardType.CREATURE], [], power=1, toughness=1)

ox = Card("Ox", "1W", [CardType.CREATURE], [], power=2, toughness=2)
crab = Card("Crab", "1U", [CardType.CREATURE], [], power=1, toughness=3)
dwarf = Card("Dwarf", "1R", [CardType.CREATURE], [], power=3, toughness=1)
bear = Card("Bear", "1G", [CardType.CREATURE], [], power=2, toughness=2)

horse = Card("Horse", "2W", [CardType.CREATURE], [], power=3, toughness=3)
serpent = Card("Serpent", "2U", [CardType.CREATURE], [], power=2, toughness=5)
drake = Card("Drake", "2R", [CardType.CREATURE], [], power=4, toughness=2)
ent = Card("Ent", "2G", [CardType.CREATURE], [], power=3, toughness=3)

angel = Card("Angel", "3W", [CardType.CREATURE], [], power=4, toughness=4)
sphinx = Card("Sphinx", "3U", [CardType.CREATURE], [], power=3, toughness=6)
dragon = Card("Dragon", "3R", [CardType.CREATURE], [], power=7, toughness=1)
dinosaur = Card("Dinosaur", "3G", [CardType.CREATURE], [], power=5, toughness=5)

# lightning_bolt = Card("Lightning Bolt", [ManaCost.RED], [CardType.INSTANT], [lightning_ability])
# rals_reinforcements = Card("Ral's Reinforcements", [ManaCost.GENERIC, ManaCost.RED], [
# CardType.SORCERY], [reinforcements_ability])

destroy = Card("Destroy", "1", [CardType.SORCERY], [destroy_ability])
draw = Card("Draw", "1", [CardType.INSTANT], [draw_card_ability])


aegis_turtle = Card("Aegis Turtle", "U", [CardType.CREATURE, CreatureType.TURTLE], [], power=0, toughness=5)
ambush_wolf = Card("Ambush Wolf", "2G", [CardType.CREATURE, CreatureType.WOLF], [flash, ambush_wolf_etb], power=4, toughness=2)
apothecary_stomper = Card("Apothecary Stomper", "4GG", [CardType.CREATURE, CreatureType.ELEPHANT], [
                          vigilance, apothecary_stomper_etb], power=4, toughness=4)
armasaur_guide = Card("Armasaur Guide", "4W", [CardType.CREATURE, CreatureType.DINOSAUR],
                      [vigilance, armasaur_guide_attack], power=4, toughness=4)
axgard_cavalry = Card("Axgard Cavalry", "1R", [CardType.CREATURE, CreatureType.DWARF,
                      CreatureType.BERSERKER], [axgard_cavalry_tap], power=2, toughness=2)
bake_into_a_pie = Card("Bake into a Pie", "2BB", [CardType.INSTANT], [bake_into_a_pie_ability])
banishing_light = Card("Banishing Light", "2W", [CardType.ENCHANTMENT], [banishing_light_ability])
beast_kin_ranger = Card("Beast-Kin Ranger", "2G", [CardType.CREATURE, CreatureType.ELF,
                        CreatureType.RANGER], [trample, beastkin_ranger_pump], power=3, toughness=3)
bigfin_bouncer = Card("Bigfin Bouncer", "3U", [CardType.CREATURE, CreatureType.SHARK,
                      CreatureType.PIRATE], [bigfin_bouncer_etb], power=3, toughness=2)
bite_down = Card("Bite Down", "1G", [CardType.INSTANT], [bite_down_ability])
bloodfell_caves = Card("Bloodfell Caves", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, rakdos_land_ability])
blossoming_sands = Card("Blossoming Sands", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, selesnya_land_ability])
broken_wings = Card("Broken Wings", "2G", [CardType.INSTANT], [broken_wings_ability])
burglar_rat = Card("Burglar Rat", "1B", [CardType.CREATURE, CreatureType.RAT], [burglar_etb], power=1, toughness=1)
burst_lightning = Card("Burst Lightning", "R", [CardType.INSTANT], [burst_lightning_ability, kicker("4")])
bushwhack = Card("Bushwhack", "G", [CardType.SORCERY], [bushwhack_ability])
cackling_prowler = Card("Cackling Prowler", "3G", [CardType.CREATURE, CreatureType.HYENA, CreatureType.ROGUE], [
                        ward("2"), cackling_prowler_morbid], power=4, toughness=3)
campus_guide = Card("Campus Guide", "2", [CardType.ARTIFACT, CardType.CREATURE,
                    CreatureType.GOLEM], [campus_guide_etb], power=2, toughness=1)
cathar_commando = Card("Cathar Commando", "1W", [CardType.CREATURE, CreatureType.HUMAN,
                       CreatureType.SOLDIER], [flash, cathar_sac], power=3, toughness=1)
courageous_goblin = Card("Courageous Goblin", "1R", [CardType.CREATURE, CreatureType.GOBLIN], [
                         courageous_goblin_attack], power=2, toughness=2)
crackling_cyclops = Card("Crackling Cyclops", "2R", [CardType.CREATURE, CreatureType.CYCLOPS,
                         CreatureType.WIZARD], [crackling_cyclops_pump], power=0, toughness=4)
crypt_feaster = Card("Crypt Feaster", "3B", [CardType.CREATURE, CreatureType.ZOMBIE],
                     [menace, crypt_feaster_threshold], power=3, toughness=4)
dazzling_angel = Card("Dazzling Angel", "2W", [CardType.CREATURE, CreatureType.ANGEL], [flying, dazzling_angel_gain], power=2, toughness=3)
dismal_backwater = Card("Dismal Backwater", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, dimir_land_ability])
dwynens_elite = Card("Dwynen's Elite", "1G", [CardType.CREATURE, CreatureType.ELF,
                     CreatureType.WARRIOR], [dwynens_elite_etb], power=2, toughness=2)
eaten_alive = Card("Eaten Alive", "B", [CardType.SORCERY], [eaten_alive_ability, eaten_alive_extra_cost])
elementalist_adept = Card("Elementalist Adept", "1U", [CardType.CREATURE, CreatureType.HUMAN, CreatureType.WIZARD], [
                          flash, prowess], power=2, toughness=1)
elfsworn_giant = Card("Elfsworn Giant", "3GG", [CardType.CREATURE, CreatureType.GIANT],
                      [reach, elfsworn_giant_landfall], power=5, toughness=3)
erudite_wizard = Card("Erudite Wizard", "2U", [CardType.CREATURE, CreatureType.HUMAN,
                      CreatureType.WIZARD], [erudite_wizard_2card], power=2, toughness=3)
evolving_wilds = Card("Evolving Wilds", None, [CardType.LAND], [evolving_wilds_sac])
fake_your_own_death = Card("Fake Your Own Death", "1B", [CardType.INSTANT], [fake_your_own_death_ability])
fanatical_firebrand = Card("Fanatical Firebrand", "R", [CardType.CREATURE, CreatureType.GOBLIN, CreatureType.PIRATE], [
                           haste, fanatical_firebrand_sac], power=1, toughness=1)
felidar_savior = Card("Felidar Savior", "3W", [CardType.CREATURE, CreatureType.CAT, CreatureType.BEAST], [
                      lifelink, felidar_savior_etb], power=2, toughness=3)
firebrand_archer = Card("Firebrand Archer", "1R", [CardType.CREATURE, CreatureType.HUMAN,
                        CreatureType.ARCHER], [firebrand_archer_ping], power=2, toughness=1)
fleeting_distraction = Card("Fleeting Distraction", "U", [CardType.INSTANT], [fleeting_distraction_ability])
fleeting_flight = Card("Fleeting Flight", "W", [CardType.INSTANT], [fleeting_flight_ability])
giant_growth = Card("Giant Growth", "G", [CardType.INSTANT], [giant_growth_ability])
gleaming_barrier = Card("Gleaming Barrier", "2", [CardType.ARTIFACT, CardType.CREATURE, CreatureType.WALL], [
                        defender, gleaming_barrier_death], power=0, toughness=4)
gnarlid_colony = Card("Gnarlid Colony", "1G", [CardType.CREATURE, CreatureType.BEAST], [
                      kicker("2G"), gnarlid_kicked_enters, gnarlid_counter_lord], power=2, toughness=2)
goblin_boarders = Card("Goblin Boarders", "2R", [CardType.CREATURE, CreatureType.GOBLIN,
                       CreatureType.PIRATE], [goblin_boarders_enters], power=3, toughness=2)
goblin_surprise = Card("Goblin Surprise", "2R", [CardType.INSTANT], [goblin_surprise_ability])
goldvein_pick = Card("Goldvein Pick", "2", [CardType.ARTIFACT, ArtifactType.EQUIPMENT],
                     [goldvein_equip_buff, goldvein_damage_trigger, equip("1")])
gorehorn_raider = Card("Gorehorn Raider", "4R", [CardType.CREATURE, CreatureType.MINOTAUR,
                       CreatureType.PIRATE], [gorehorn_raider_etb], power=4, toughness=4)
grow_from_the_ashes = Card("Grow from the Ashes", "2G", [CardType.SORCERY], [grow_from_the_ashes_ability, kicker("2")])
gutless_plunderer = Card("Gutless Plunderer", "2B", [CardType.CREATURE, CreatureType.SKELETON, CreatureType.PIRATE], [
                         deathtouch, gutless_plunderer_etb], power=2, toughness=2)
hare_apparent = Card("Hare Apparent", "1W", [CardType.CREATURE, CreatureType.RABBIT,
                     CreatureType.NOBLE], [hare_apparent_etb], power=2, toughness=2)
healers_hawk = Card("Healer's Hawk", "W", [CardType.CREATURE, CreatureType.BIRD], [flying, lifelink], power=1, toughness=1)
helpful_hunter = Card("Helpful Hunter", "1W", [CardType.CREATURE, CreatureType.CAT], [helpful_hunter_etb], power=1, toughness=1)
hungry_ghoul = Card("Hungry Ghoul", "1B", [CardType.CREATURE, CreatureType.ZOMBIE], [hungry_ghoul_sac], power=2, toughness=2)
icewind_elemental = Card("Icewind Elemental", "4U", [CardType.CREATURE, CreatureType.ELEMENTAL], [
                         flying, icewind_elemental_etb], power=3, toughness=4)
incinerating_blast = Card("Incinerating Blast", "4R", [CardType.SORCERY], [incinerating_blast_ability])
infestation_sage = Card("Infestation Sage", "B", [CardType.CREATURE, CreatureType.ELF,
                        CreatureType.WARLOCK], [infestation_sage_death], power=1, toughness=1)
inspiring_paladin = Card("Inspiring Paladin", "2W", [CardType.CREATURE, CreatureType.HUMAN, CreatureType.KNIGHT], [
                         paladin_self_anthem, paladin_counter_lord], power=3, toughness=3)
involuntary_employment = Card("Involuntary Employment", "3R", [CardType.SORCERY], [involuntary_employment_ability])
jungle_hollow = Card("Jungle Hollow", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, golgari_land_ability])
lightshell_duo = Card("Lightshell Duo", "3U", [CardType.CREATURE, CreatureType.RAT,
                      CreatureType.OTTER], [prowess, lightshell_duo_etb], power=3, toughness=4)
llanowar_elves = Card("Llanowar Elves", "G", [CardType.CREATURE, CreatureType.ELF,
                      CreatureType.DRUID], [forest_ability], power=1, toughness=1)
luminous_rebuke = Card("Luminous Rebuke", "4W", [CardType.INSTANT], [luminous_rebuke_ability, luminous_cost_reduction])
macabre_waltz = Card("Macabre Waltz", "1B", [CardType.SORCERY], [macabre_waltz_ability])
make_your_move = Card("Make Your Move", "2W", [CardType.INSTANT], [make_your_move_ability])
marauding_blight_priest = Card("Marauding Blight-Priest", "2B",
                               [CardType.CREATURE, CreatureType.VAMPIRE, CreatureType.CLERIC], [blight_priest_ability], power=3, toughness=2)
mocking_sprite = Card("Mocking Sprite", "2U", [CardType.CREATURE, CreatureType.FAERIE, CreatureType.ROGUE], [
                      flying, mocking_sprite_discount], power=2, toughness=1)
pilfer = Card("Pilfer", "1B", [CardType.SORCERY], [pilfer_ability])
prideful_parent = Card("Prideful Parent", "2W", [CardType.CREATURE, CreatureType.CAT],
                       [vigilance, prideful_parent_etb], power=2, toughness=2)
quick_draw_katana = Card("Quick-Draw Katana", "2", [CardType.ARTIFACT, ArtifactType.EQUIPMENT],
                         [katana_equip_buff_1, katana_equip_buff_2, equip("2")])
refute = Card("Refute", "1UU", [CardType.INSTANT], [refute_ability])
rugged_highlands = Card("Rugged Highlands", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, gruul_land_ability])
run_away_together = Card("Run Away Together", "1U", [CardType.INSTANT], [run_away_together_ability])
sanguine_syphoner = Card("Sanguine Syphoner", "1B", [CardType.CREATURE, CreatureType.VAMPIRE,
                         CreatureType.WARLOCK], [syphoner_attack], power=1, toughness=3)
scoured_barrens = Card("Scoured Barrens", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, orzhov_land_ability])
soul_shackled_zombie = Card("Soul-Shackled Zombie", "3B", [CardType.CREATURE,
                            CreatureType.ZOMBIE], [soul_shackled_etb], power=4, toughness=2)
sower_of_chaos = Card("Sower of Chaos", "3R", [CardType.CREATURE, CreatureType.DEVIL], [sower_of_chaos_activated], power=4, toughness=3)
spitfire_lagac = Card("Spitfire Lagac", "3R", [CardType.CREATURE, CreatureType.LIZARD], [spitfire_landfall], power=3, toughness=4)
squad_rallier = Card("Squad Rallier", "3W", [CardType.CREATURE, CreatureType.HUMAN,
                     CreatureType.SCOUT], [squad_rallier_activated], power=3, toughness=4)
stab = Card("Stab", "B", [CardType.INSTANT], [stab_ability])
strix_lookout = Card("Strix Lookout", "1U", [CardType.CREATURE, CreatureType.BIRD], [flying, vigilance, strix_loot], power=1, toughness=2)
sure_strike = Card("Sure Strike", "1R", [CardType.INSTANT], [sure_strike_ability])
swiftwater_cliffs = Card("Swiftwater Cliffs", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, izzet_land_ability])
think_twice = Card("Think Twice", "1U", [CardType.INSTANT], [think_twice_ability, flashback("2U")])
thornwood_falls = Card("Thornwood Falls", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, simic_land_ability])
thrill_of_possibility = Card("Thrill of Possibility", "1R", [CardType.INSTANT], [thrill_ability, thrill_extra_cost])
tolarian_terror = Card("Tolarian Terror", "6U", [CardType.CREATURE, CreatureType.SERPENT],
                       [tolarian_cost_reduction, ward("2")], power=5, toughness=5)
tranquil_cove = Card("Tranquil Cove", None, [CardType.LAND], [enters_tapped_replacement, gain_1_etb, azorius_land_ability])
treetop_snarespinner = Card("Treetop Snarespinner", "3G", [CardType.CREATURE, CreatureType.SPIDER], [
                            reach, deathtouch, treetop_snarespinner_activated], power=1, toughness=4)
uncharted_voyage = Card("Uncharted Voyage", "3U", [CardType.INSTANT], [uncharted_voyage_ability])
vampire_soulcaller = Card("Vampire Soulcaller", "4B", [CardType.CREATURE, CreatureType.VAMPIRE, CreatureType.WARLOCK], [
                          flying, cant_block, soulcaller_etb], power=3, toughness=2)
vanguard_seraph = Card("Vanguard Seraph", "3W", [CardType.CREATURE, CreatureType.ANGEL, CreatureType.WARRIOR], [
                       flying, vanguard_seraph_trigger], power=3, toughness=3)
