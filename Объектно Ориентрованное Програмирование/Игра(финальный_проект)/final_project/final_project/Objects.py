from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


# FIXME
# add class
class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def draw(self, display):
        display.blit(self.sprite,
                     (self.position[0] * display.engine.sprite_size, self.position[1] * display.engine.sprite_size))
#


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp
        self.damage = self.calc_damage()

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def calc_damage(self):
        return self.stats['strength']


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
            self.damage = self.calc_damage()
            yield "level up!"


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @property
    def damage(self):
        return self.base.damage

    @damage.setter
    def damage(self, value):
        self.base.damage = value

    @abstractmethod
    def apply_effect(self):
        pass


# FIXME
# add classes
class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

    def interact(self, engine, hero):
        engine.duel(self, hero)


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5
        self.stats['endurance'] += 5
        self.stats['intelligence'] -= 2
        self.calc_max_HP()
        self.damage = self.calc_damage()

    def calc_max_HP(self):
        super().calc_max_HP()
        if self.max_hp < self.hp:
            self.hp = self.max_hp


class Blessing(Effect):
    def apply_effect(self):
        for stat in self.stats:
            self.stats[stat] += 3
        self.calc_max_HP()
        self.damage = self.calc_damage()

    def calc_max_HP(self):
        super().calc_max_HP()
        if self.max_hp < self.hp:
            self.hp = self.max_hp


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 5
        self.stats['endurance'] -= 5
        self.calc_max_HP()
        self.damage = self.calc_damage()

    def calc_max_HP(self):
        super().calc_max_HP()
        if self.max_hp < self.hp:
            self.hp = self.max_hp


class Wisdom(Effect):
    def apply_effect(self):
        self.stats['intelligence'] += 5
