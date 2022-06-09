import Service
import random


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    mini_map = None

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] -= 1
        self.interact()

    def move_down(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] += 1
        self.interact()

    def move_left(self):
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position[0] -= 1
        self.interact()

    def move_right(self):
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    def load_mini_map(self, game_map):
        self.mini_map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)

    # ENEMIES
    # интеракция Enemy и Hero
    def duel(self, enemy, hero):
        self._fight(enemy, hero)
        if hero.hp <= 0:
            Service.death_screen(self, hero)
            self.notify('You are dead =(')
            return
        self._add_exp(enemy, hero)
        self.score += 1

    # опыт за убийство Enemy
    def _add_exp(self, enemy, hero):
        hero.exp += enemy.xp
        while hero.exp >= 100 * (2 ** (hero.level - 1)):
            message = next(hero.level_up())
            self.notify(message)
            self.notify('')

    # непосредственно сражение
    def _fight(self, enemy, hero):
        self.notify('The battle begins!')
        self.notify(f'Enemy HP: {enemy.hp}')
        i = 0
        while enemy.hp > 0 and hero.hp > 0:
            i += 1
            self.notify(f'{i} round!')
            if random.randint(0, 50) <= enemy.stats['luck']:
                self.notify('Enemy dodged your attack...')
            else:
                enemy.hp = enemy.hp - hero.damage
                self.notify(f'You damaged {hero.damage}HP to the enemy')

            if random.randint(0, 50) <= hero.stats['luck']:
                self.notify('You dodged the attack')
            else:
                hero.hp = hero.hp - enemy.damage
                self.notify(f'Enemy damaged {enemy.damage}HP to you')
        self.notify('Battle is finished')
        self.notify('')
