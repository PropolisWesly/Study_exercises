import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


# загрузка экрана смерти (hp <= 0)
def death_screen(engine, hero):
    hero.hp = 0
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    _map = DeathMap().Map().get_map()[0]
    engine.load_map(_map)
    mini_map = DeathMap().Map().get_map()[1]
    engine.load_mini_map(mini_map)
    engine.add_objects(DeathMap().Objects().get_objects(_map))
    engine.add_hero(hero)


def reload_game(engine, hero):
    global level_list
    level_list_max = len(level_list) - 1
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    generator = level_list[min(engine.level, level_list_max)]
    _map = generator['map'].get_map()[0]
    engine.load_map(_map)
    mini_map = generator['map'].get_map()[1]
    engine.load_mini_map(mini_map)
    engine.add_objects(generator['obj'].get_objects(_map))
    engine.add_hero(hero)


# действие союзника-волка
def smart_quote(engine, hero):
    engine.notify('The Great Wolf wants')
    engine.notify('to share his wisdom!')
    messages = [['Если волк молчит, то', 'его лучше не перебивать'],
               ['Легко вставать, когда', 'ты не ложился'],
               ['Иногда жизнь это жизнь', 'а ты в ней иногда'],
               ['Бесплатный сыр бывает', 'только бесплатным'],
               ['Я не боюсь ударов', 'в спину, гораздо страшнее,', 'если это моя спина...']]
    quote_number = random.randint(0, 4)
    for mes in messages[quote_number]:
        engine.notify(mes)
    engine.hero = Objects.Wisdom(hero)
    engine.notify('It felt deep...')
    engine.notify('wisdom applied')
    engine.notify('')
    engine.score += 0.2


def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")
    engine.notify("")


def apply_blessing(engine, hero):
    if hero.gold >= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(hero)
            engine.notify("Blessing applied")
            engine.notify("")
        else:
            engine.hero = Objects.Berserk(hero)
            engine.notify("Berserk applied")
            engine.notify("")
    else:
        engine.score -= 0.1


def remove_effect(engine, hero):
    if hero.gold >= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5**engine.level) - \
            2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_HP()
        engine.notify("Effect removed")
        engine.notify("")


def add_gold(engine, hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(hero)
        engine.notify("You were cursed")
        engine.notify("")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")
        engine.notify("")


class MapFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):

        # FIXME
        # get _map and _obj
        # Вроде, пофиксил
        value = loader.construct_mapping(node)
        _obj = cls.create_objects()
        if value != {}:
            _obj.config = value
        return {'map': cls.create_map(), 'obj': _obj}

    @classmethod
    def create_map(cls):
        return cls.Map()

    @classmethod
    def create_objects(cls):
        return cls.Objects()


# карта после смерти героя
class DeathMap(MapFactory):

    class Map:  #11x32
        def __init__(self):
            self.Map = ['00000000000000000000000000000000',
                        '0                              0',
                        '0                              0',
                        '0  0   0  00 00  00000  00000  0',
                        '0  00 00  00000  0      0   0  0',
                        '0   000   0 0 0  00000  00000  0',
                        '0    0    0   0  0      0      0',
                        '0  000    0   0  00000  0      0',
                        '0                              0',
                        '0                              0',
                        '00000000000000000000000000000000'
                        ]

            self.Map = list(map(list, self.Map))
            self.mini_map = [['' for _ in range(32)] for _ in range(11)]

            for i in range(len(self.Map)):
                for j in range(len(self.Map[i])):
                    if self.Map[i][j] == '0':
                        self.Map[i][j] = wall
                        self.mini_map[i][j] = 'wall'
                    else:
                        self.Map[i][j] = floor1
                        self.mini_map[i][j] = ''

        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class EndMap(MapFactory):

    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            self.mini_map = [['' for _ in range(39)] for _ in range(11)]

            for i in range(len(self.Map)):
                for j in range(len(self.Map[i])):
                    if self.Map[i][j] == '0':
                        self.Map[i][j] = wall
                        self.mini_map[i][j] = 'wall'
                    else:
                        self.Map[i][j] = floor1
                        self.mini_map[i][j] = ''
         
        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:  # 20x30

        def __init__(self):
            self.Map = [[0 for _ in range(30)] for _ in range(20)]
            self.mini_map = [['' for _ in range(30)] for _ in range(20)]
            for i in range(30):
                for j in range(20):
                    if i == 0 or j == 0 or i == 29 or j == 19:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

                    if self.Map[j][i] == wall:
                        self.mini_map[j][i] = 'wall'

            self.Map[1][1] = [floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 7)]

        def get_map(self):
            return self.Map, self.mini_map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_friendly(self, _map, friend_type):
            # расстановка сундуков и лестниц или нпс
            for obj_name in object_list_prob[friend_type]:
                prop = object_list_prob[friend_type][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 28), random.randint(1, 18))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 28),
                                     random.randint(1, 18))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 28),
                                         random.randint(1, 18))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

        def get_enemy(self, _map):
            # расстановка вражин
            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, 28), random.randint(1, 18))  # странно, но почему бы и нет
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 28),
                                     random.randint(1, 18))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 28),
                                         random.randint(1, 18))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects

        def get_objects(self, _map):
            self.get_friendly(_map, 'objects')
            self.get_friendly(_map, 'ally')
            self.get_enemy(_map)
            return self.objects


# FIXME
# add classes for YAML !empty_map and !special_map{}
# пустая карта имеет только лестницу
class EmptyMap(MapFactory):
    yaml_tag = '!empty_map'

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(30)] for _ in range(20)]
            self.mini_map = [['' for _ in range(30)] for _ in range(20)]
            for i in range(30):
                for j in range(20):
                    if i == 0 or j == 0 or i == 29 or j == 19:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

                    if self.Map[j][i] == wall:
                        self.mini_map[j][i] = 'wall'

            self.Map[1][1] = [floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 7)]

        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            # расстановка сундуков и лестниц или нпс
            prop = object_list_prob['objects']['stairs']
            for i in range(random.randint(prop['min-count'], prop['max-count'])):
                coord = (random.randint(1, 28), random.randint(1, 18))
                intersect = True
                while intersect:
                    intersect = False
                    if _map[coord[1]][coord[0]] == wall:
                        intersect = True
                        coord = (random.randint(1, 28),
                                    random.randint(1, 18))
                        continue
                    for obj in self.objects:
                        if coord == obj.position or coord == (1, 1):
                            intersect = True
                            coord = (random.randint(1, 28),
                                        random.randint(1, 18))

                self.objects.append(Objects.Ally(
                    prop['sprite'], prop['action'], coord))

                return self.objects


# в специальной карте можно задавать тип и количество врагов через objects.config и yaml дока
class SpecialMap(MapFactory):
    yaml_tag = '!special_map'

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(30)] for _ in range(20)]
            self.mini_map = [['' for _ in range(30)] for _ in range(20)]
            for i in range(30):
                for j in range(20):
                    if i == 0 or j == 0 or i == 29 or j == 19:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

                    if self.Map[j][i] == wall:
                        self.mini_map[j][i] = 'wall'

            self.Map[1][1] = [floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 7)]

        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []
            self.config = {}

        def get_enemy(self, _map):
            # расстановка вражин
            for obj_name in self.config:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(self.config[obj_name]):
                    coord = (random.randint(1, 28), random.randint(1, 18))  # странно, но почему бы и нет
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 28),
                                     random.randint(1, 18))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 28),
                                         random.randint(1, 18))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects

        def get_friendly(self, _map, friend_type):
            # расстановка сундуков и лестниц или нпс
            for obj_name in object_list_prob[friend_type]:
                prop = object_list_prob[friend_type][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 28), random.randint(1, 18))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 28),
                                     random.randint(1, 18))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 28),
                                         random.randint(1, 18))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

        def get_objects(self, _map):
            self.get_friendly(_map, 'objects')
            self.get_friendly(_map, 'ally')
            self.get_enemy(_map)
            return self.objects

wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    wall[0] = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1[0] = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2[0] = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3[0] = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read())
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp,
                           'smart_quote': smart_quote}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'][0] = create_sprite(
            os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)  # вместо png поставили объект Surface
        prop['action'] = object_list_actions[prop_tmp['action']]  # вместо строки записали функцию

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'][0] = create_sprite(
            os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)   # вместо png поставили объект Surface
        prop['action'] = object_list_actions[prop_tmp['action']]  # вместо строки записали функцию

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy]
        prop['sprite'][0] = create_sprite(
            os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)  # вместо png поставили объект Surface

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read())['levels']  # вернуть объекты Map() и  Objects()
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
