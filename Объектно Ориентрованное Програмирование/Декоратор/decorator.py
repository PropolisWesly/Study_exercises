from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        pass

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Berserk']

    def get_stats(self):
        stats = self.base.get_stats()
        for stat in ["Strength", "Endurance", "Agility", "Luck"]:
            stats[stat] += 7
        for stat in ["Perception", "Charisma", "Intelligence"]:
            stats[stat] -= 3
        stats['HP'] += 50
        return stats


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Blessing']

    def get_stats(self):
        stats = self.base.get_stats()
        for stat in ["Strength", "Endurance", "Agility", "Luck", "Perception", "Charisma", "Intelligence"]:
            stats[stat] += 2
        return stats


class Weakness(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']

    def get_stats(self):
        stats = self.base.get_stats()
        for stat in ["Strength", "Endurance", "Agility"]:
            stats[stat] -= 4
        return stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']

    def get_stats(self):
        stats = self.base.get_stats()
        for stat in ["Strength", "Endurance", "Agility", "Luck", "Perception", "Charisma", "Intelligence"]:
            stats[stat] -= 2
        return stats


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']

    def get_stats(self):
        stats = self.base.get_stats()
        stats['Luck'] -= 10
        return stats
