class Keyword_Ability:
    def __init__(self, keyword_ability):
        self.keyword_ability = keyword_ability

    def copy(self):
        return Keyword_Ability(self.keyword_ability)
