import items
import world


class Player:
    def __init__(self):
        self.hp = 100
        self.victory = False
        self.x, self.y = world.starting_position
        self.inventory = [items.Rock()]
        self.gold = 15

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print('Inventory:')
        for item in self.inventory:
            print('*' + str(item))
        print('Gold: {}'.format(self.gold))

    def heal(self):
        consumables = [i for i in self.inventory if isinstance(i, items.Consumable)]
        if not consumables:
            print('You don\'t have anything to heal yourself with.')
            return
        print('Choose an item to use to heal:')
        for i, item in enumerate(consumables):
            print('{}. {}'.format(i, item))
        consumed = False
        while not consumed:
            choice = input('')
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print('Current HP: {}'.format(self.hp))
                consumed = True
            except(ValueError, IndexError):
                print('Invalid choice, try again.')

    def strongestweapon(self):
        best_weapon = None
        max_damage = 0
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    max_damage = item.damage
                    best_weapon = item
            except AttributeError:
                pass
        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self):
        best_weapon = self.strongestweapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print('You use {} against {}!'.format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print('You killed {}!'.format(enemy.name))
        else:
            print('{} HP is {}.'.format(enemy.name, enemy.hp))

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
