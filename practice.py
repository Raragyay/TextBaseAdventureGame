import random

import enemies
import items
import npc


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return '''You find yourself in a cave with a flickering torch on the wall. 
        You can make out four paths, each equally as dark and foreboding.'''

    def modify_player(self, player):
        # This room has no action on the player.
        pass


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = '''A giant spider jumps down from its web in front of you!'''
            self.dead_text = '''The corpse of a dead spider rots on the ground.'''
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                              "...suddenly you are lost in s swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster " \
                              "from his slumber!"
            self.dead_text = "Defeated, the monster has reverted " \
                             "into an ordinary rock."
        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print('Enemy does {} damage. You have {} HP remaining.'
                  .format(self.enemy.damage, player.hp))


class VictoryTile(MapTile):
    def intro_text(self):
        return '''
You see a bright light in the distance...
... it grows as you get closer! It's sunlight!

Victory is yours!
        '''

    def modify_player(self, player):
        player.victory = True


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold += self.gold
            print('+{} gold added. You now have {} gold.'.format(self.gold, player.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
            """


class LootTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.itemclaimed = False
        r = random.random()
        if r < 0.70:
            self.item = items.Dagger()
            self.itemtext = '''
            You enter the cave. 
            You\'re about to pass when you see a dagger on the floor. 
            It looks like it\'s been lying there forever.
            '''
        else:
            self.item = items.RustySword()
            self.itemtext = '''
            You enter the cave.
            What's that? It's a hilt in the stone.
            You try to pull it out with all your might.
            To your surprise, it slides out easily! That's a sword for you!
            '''

    def modify_player(self, player):
        if not self.itemclaimed:
            self.itemclaimed = True
            player.inventory.append(self.item)
            print('You have obtained a {}.'.format(self.item.name))

    def intro_text(self):
        if not self.itemclaimed:
            print(self.itemtext)
        else:
            print('''You scour the area, hoping for another miracle. Alas, none appear. ''')


def swap(seller, buyer, item):
    if item.value > buyer.gold:
        print('That\'s too expensive!')
        return
    seller.inventory.remove(item)
    buyer.inventory.append(item)
    seller.gold += item.value
    buyer.gold += item.value
    print('Trade Complete!')


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def check_if_trade(self, player):
        while True:
            print('Would you like to (B)uy, (S)ell, or (Q)uit?')
            ui = input()
            if ui in ['q', 'Q']:
                return
            elif ui in ['b', 'B']:
                print('Here\'s what\'s available to buy: ')
                self.trade(seller=self.trader, buyer=player)
            elif ui in ['s', 'S']:
                print('What would you like to sell?')
                self.trade(seller=player, buyer=self.trader)
            else:
                print('Invalid Choice!')

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print('{}. {} - {} Gold.'.format(i, item.name, item.value))
        while True:
            ui = input('Please choose an item or press q to quit.')
            if ui in ['q', 'Q']:
                return
            else:
                try:
                    choice = int(ui)
                    to_swap = seller.inventory[choice - 1]
                    swap(seller, buyer, to_swap)
                except ValueError:
                    print('Invalid choice!')

    def intro_text(self):
        return '''
        A frail not-quite-human, not-quite-creature sits in the corner,
        clinking his gold coins together. He looks willing to trade. 
        '''


starting = False
victory = False
tilenames = {
    'ST': StartTile,
    'VT': VictoryTile,
    'FG': FindGoldTile,
    'EN': EnemyTile,
    'TT': TraderTile,
    'FL': LootTile,
    '  ': None
}


def generateworld():
    world = []
    while True:
        try:
            size = int(input('What size should the map be? Please give a number between 5 and 25.\n'))
            if 5 <= size <= 25:
                break
            else:
                print('I said, between 5 and 25. ')
        except ValueError:
            print('Please give me a size. An integer, if you please')
    for i in range(size):
        row = []
        for j in range(size):
            row.append(randomizetile(size))
        world.append(row)
        print(row)
    return world


def randomizetile(size):
    r = random.random()
    global starting
    global victory
    mapsize = size ** 2
    if not starting:
        if r < 1 - (0.01 ** (1 / mapsize)):
            starting = True
            return 'ST'
    if not victory:
        if r > 0.01 ** (1 / mapsize):
            victory = True
            return 'VT'
    if r < 0.15:
        return 'FL'
    elif r < 0.45:
        return 'EN'
    elif r < 0.65:
        return '  '
    elif r < 0.90:
        return 'FG'
    else:
        return 'TT'


world_map = []


def parsetiles():
    while True:
        world = generateworld()
        for y, r in enumerate(world):
            row = []
            for x, cell in enumerate(r):
                tile_name = tilenames[cell]
                if tile_name == StartTile:
                    global starting_position
                    starting_position = (x, y)
                row.append(tile_name(x, y) if tile_name else None)
            world_map.append(row)
        starting_node = tile_at(starting_position[0], starting_position[1])
        if bfs(starting_node):
            break


def findadjacenttiles(x, y):
    arr = set()
    arr.add(tile_at(x + 1, y))
    arr.add(tile_at(x - 1, y))
    arr.add(tile_at(x, y - 1))
    arr.add(tile_at(x, y + 1))
    arr = {i for i in arr if i}
    return arr


def bfs(start):
    queue = [start]
    visited = set()
    while queue:
        node = queue.pop(0)
        for connection in findadjacenttiles(node.x, node.y) - visited:
            visited.add(connection)
            queue.append(connection)
            if isinstance(connection, VictoryTile):
                return True
    return False


def strtile_at(x, y, world):
    if x < 0 or y < 0:
        return None
    try:
        return world[y][x]
    except IndexError:
        return None


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
