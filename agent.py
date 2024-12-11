import os

from enums import AbilityKeyword
input_file = open("input.txt")

file_size = os.path.getsize("input.txt")


def user_input(prompt) -> str:
    res = input_file.readline()[:-1]
    if res == "":
        res = input(prompt)
    with open("user_input.txt", "a") as file:
        file.write(res+"\n")
    return res


def user_display(game):
    if file_size == input_file.tell():
        game.display()


class Agent:
    def __init__(self, name, deck) -> None:
        self.name = name
        self.deck = deck

    def get_name(self):
        return self.name

    def get_deck(self):
        return self.deck.copy()
    # Decision making functions

    def choose_one(self, choices, message="Choose One:"):
        if len(choices) == 0:
            raise Exception("Player can't make choice.")
        if len(choices) == 1:
            return choices[0]
        while True:
            for i, choice in enumerate(choices):
                print(f"{i}: {choice}")
            choice_num = user_input(f"{self.name} {message}")
            if choice_num.isnumeric():
                choice_num = int(choice_num)
                if choice_num < len(choices):
                    return choices[choice_num]
                else:
                    print("Out of Bounds.")
            else:
                print("Invalid Answer.")

    def choose_yes_or_no(self, choice, message="Choose Yes or No:"):
        while True:
            print(f"{choice}")
            choice = user_input(f"{self.name} {message}")
            if choice[0].lower() == "y":
                return True
            elif choice[0].lower() == "n":
                return False
            else:
                print("Invalid Answer.")

    def choose_any(self, choices, message="Choose Any Number:"):
        if len(choices) == 0:
            return []
        while True:
            for i, choice in enumerate(choices):
                print(f"{i}: {choice}")
            choice_nums = user_input(f"{self.name} {message}")
            if choice_nums == "none":
                return []
            chosen = []
            for choice_num in choice_nums.split(" "):
                if choice_num.isnumeric():
                    choice_num = int(choice_num)
                    if choice_num < len(choices):
                        chosen.append(choices[choice_num])
                    else:
                        print("Out of Bounds.")
                        break
                else:
                    print("Invalid Answer.")
                    break
            else:
                return chosen

    def choose_x(self, options, amount, message="Choose X:"):
        if len(options) < amount:
            raise Exception("Player can't make more choices than options")
        if len(options) == amount:
            return options
        choices = []
        chosen_nums = []
        while True:
            for i, choice in enumerate(options):
                print(f"{i}: {choice}")
            choice_nums = user_input(f"{self.name} {message}")
            for choice_num in choice_nums.split(" "):
                if choice_num.isnumeric():
                    choice_num = int(choice_num)
                    if choice_num in chosen_nums:
                        print("Duplicate Answer")
                        break
                    choices.append(options[choice_num])
                    chosen_nums.append(choice_num)
                else:
                    print("Invalid Answer.")
                    break
            else:
                return choices

    def choose_order(self, choices, message="Choose Order:"):
        if len(choices) <= 1:
            return choices
        while True:
            for i, choice in enumerate(choices):
                print(f"{i}: {choice}")
            choice_nums = user_input(f"{self.name} {message}")
            if len(choice_nums.split(" ")) != len(choices):
                print("Order all options.")
                break
            order = []
            for choice_num in choice_nums.split(" "):
                if choice_num.isnumeric():
                    choice_num = int(choice_num)
                    if choice_num < len(choices):
                        order.append(choices[choice_num])
                    else:
                        print("Out of Bounds.")
                        break
                else:
                    print("Invalid Answer.")
                    break
            else:
                return order

    def distribute(self, total_amount, choices, message="Choose Distribution") -> list:
        if len(choices) == 0:
            raise Exception("Can't distribute among zero.")
        if len(choices) == 1:
            return [total_amount]
        while True:
            for i, choice in enumerate(choices):
                print(f"{i}: {choice}")
            print(f"Amount to distribute: {total_amount}")
            amounts = user_input(f"{self.name} {message}")
            if len(amounts.split(" ")) != len(choices):
                print("Distribute among all options.")
                continue
            distribution = []
            for amount in amounts.split(" "):
                if amount.isnumeric() and int(amount) >= 0:
                    amount = int(amount)
                    distribution.append(amount)
                else:
                    print("Invalid Answer.")
                    break
            else:
                if sum(distribution) == total_amount:
                    return distribution
                else:
                    print(
                        f"Total must be less than or equal to {total_amount}.")

    # Agent API calls

    def act(self, game, player):
        actions = game.get_priority_actions(player)
        if len(actions) == 0:
            return False
        for action in actions:
            if action.is_priority_holding:
                break
        else:
            return False
        user_display(game)
        while True:
            for i, action in enumerate(actions):
                print(f"{i}: {action}")
            choice = user_input("Act (%s)?" % self.name)
            if choice.isnumeric():
                choice = int(choice)
                if choice < len(actions):
                    return actions[choice]
                else:
                    print("Out of Bounds.")
            elif choice == "pass":
                return False
            else:
                print("Invalid Answer.")

    def mana_act(self, game, player, cost):
        abilities = game.get_mana_abilities_of(player)
        if len(abilities) == 0:
            return False
        user_display(game)
        while True:
            for i, ability in enumerate(abilities):
                print(f"{i}: {ability.name}")
            choice = user_input("Activate Mana Ability (%s)?" % self.name)
            if choice.isnumeric():
                choice = int(choice)
                if choice < len(abilities):
                    return abilities[choice]
                else:
                    print("Out of Bounds.")
            elif choice == "pass":
                return False
            else:
                print("Invalid Answer.")

    def choose_attacks(self, game, legal_attackers, targets):
        user_display(game)
        attackers = self.choose_any(legal_attackers,
                                    "Choose any to attack:")
        attacks = []
        for attacker in attackers:
            target = self.choose_one(
                targets, f"Choose a target for {attacker} to attack:")
            attacks.append((attacker, target))
        return attacks

    def choose_blocks(self, game, legal_blocks, attackers):
        user_display(game)
        blockers = self.choose_any(legal_blocks, "Choose any to block:")
        blocks = []
        for blocker in blockers:
            target = self.choose_one(
                attackers, f"Choose a target for {blocker} to block:")
            blocks.append((blocker, target))
        return blocks

    def choose_damage_assignments(self, game, damaging_creatures):
        user_display(game)
        damage_assignments = []
        for creature in damaging_creatures:
            if creature.power <= 0:
                continue
            if creature.is_unblocked:
                damage_assignments.append(
                    [creature, [[creature.power, creature.attack_target]]])
                continue
            creatures_to_damage = creature.combat_foes
            if AbilityKeyword.TRAMPLE in creature.keywords and creature.is_attacking:
                creatures_to_damage.append(creature.attack_target)
            if len(creatures_to_damage) == 0:
                continue
            if len(creatures_to_damage) == 1:
                damage_assignments.append(
                    [creature, [[creature.power, creatures_to_damage[0]]]])
                continue
            damage_assignment = self.distribute(
                creature.power, creatures_to_damage, f"Distribute damage of {creature}:")
            damages = []
            for i, damage in enumerate(damage_assignment):
                if damage <= 0:
                    continue
                defending_creature = creatures_to_damage[i]
                damages.append((damage, defending_creature))
            damage_assignments.append((creature, damages))
        return damage_assignments

    def choose_cards_to_discard(self, game, hand, discard_number):
        return self.choose_x(hand, discard_number, message=f"Choose {discard_number}")

    def choose_mana_to_pay(self, game, pool, cost):
        payment = []
        # print(pool.mana)
        for mana_sym in sorted(cost, key=lambda cost: cost.value):
            payable = pool.get_payable_to(mana_sym)
            for mana in payable:
                if mana not in payment:
                    payment.append(mana)
                    break
            else:
                return None
        return payment

    def choose_permanents_to_pay_cost(self, game, permanents, cost, cost_object):
        payment = []
        for use_cost in cost:
            options = [permanent for permanent in permanents if use_cost.acceptance_function(
                permanent, cost_object) and permanent not in payment]
            if len(options) == 0:
                return None
            permanent_to_use = self.choose_one(options)
            payment.append(permanent_to_use)
        return payment

    def choose_targets(self, game, player, targets_required, source):
        targets = []
        user_display(game)
        for target_type in targets_required:
            targets_legally_chosen = False
            target_choices = game.get_targets(player, target_type, source)
            while not targets_legally_chosen:
                target_word = []
                print(f"Choose {target_type.name}.")
                for i in range(target_type.number):
                    legal_targets = [t for t in target_choices if t not in target_word]
                    for target in legal_targets:
                        if target in target_word:
                            pass
                    if len(legal_targets) == 0:
                        return None
                    target = self.choose_one(legal_targets, f"Choose a target: ")
                    if target == None:  # TODO: None needs to be a placeholder for spells with multiple optional targets
                        continue
                    target_word.append(target)
                targets_legally_chosen = target_type.total_req_function is None or target_type.total_req_function(target_word)
            targets.extend(target_word)
        return targets

    def choose_modes(self, game, mode_choice):
        user_display(game)
        mode = self.choose_x(mode_choice.modes, mode_choice.modes_required)
        return mode

    def choose_surveil(self, cards):
        to_graveyard = self.choose_any(cards, message="Choose Cards to send to Graveyard: ")
        top_order = self.choose_order([card for card in cards if card not in to_graveyard], message="Choose order of cards on top: ")
        return to_graveyard, top_order
