class Weapon:
    def __init__(self):
        raise NotImplementedError('Do not create raw Weapon Objects')

    def __str__(self):
        return '{}\n=====\n{}\nValue: {}\nDamage:{}'.format(self.name, self.description, self.value, self.damage)


class Rock(Weapon):
    def __init__(self):
        self.name = 'Rock'
        self.description = 'A fist-sized rock, suitable for bludgeoning.'
        self.value = 0
        self.damage = 5


class Dagger(Weapon):
    def __init__(self):
        self.name = 'Dagger'
        self.description = 'A small dagger with some rust. Somewhat more dangerous than a rock.'
        self.value = 10
        self.damage = 10


class RustySword(Weapon):
    def __init__(self):
        self.name = 'Rusty Sword'
        self.description = 'A sword you found stuck in a rock. Who knows? Maybe it\'s still sharp.'
        self.value = 100
        self.damage = 20


class Consumable:
    def __init__(self):
        raise NotImplementedError('Do not create raw consumables. They\'ll make you vomit.')

    def __str__(self):
        return '{} (+{} HP)'.format(self.name, self.healing_value)


class CrustyBread(Consumable):
    def __init__(self):
        self.name = 'Crusty Bread'
        self.healing_value = 10
        self.value = 12


class HealingPotion(Consumable):
    def __init__(self):
        self.name = 'Healing Potion'
        self.healing_value = 50
        self.value = 60
