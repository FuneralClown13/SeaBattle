from random import randint, choice
from copy import copy
from itertools import count


class Ship:
    ids = count(0)

    def __init__(self, length, tp=1, x=1, y=1):
        self._id = next(self.ids)
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp  # 1 - горизонтальная; 2 - вертикальная
        self._is_move = True
        self._cells = [1] * length

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._tp == 1:
            self._x += go
        else:
            self._y += go

    def get_around_coords(self, radius=1):
        x, y = self._x, self._y
        if self._tp == 1:
            return list(
                sum([[(xi, yi) for yi in range(y - 1, y + 2)] for xi in range(x - radius, x + self._length + radius)], []))
        if self._tp == 2:
            return list(
                sum([[(xi, yi) for xi in range(x - 1, x + 2)] for yi in range(y - radius, y + self._length + radius)], []))

    def get_coords(self):
        x, y = self._x, self._y
        if self._tp == 1:
            return [(xi, y) for xi in range(x, x + self._length)]
        if self._tp == 2:
            return [(x, yi) for yi in range(y, y + self._length)]

    def is_collide(self, ship):
        ship1_coords = self.get_around_coords()
        ship2_coords = set(ship.get_coords())
        for coords in ship1_coords:
            if coords in ship2_coords:
                return True
        return False

    def is_out_pole(self, size=10):
        for x, y in self.get_coords():
            if (not 0 <= x < size) or (not 0 <= y < size):
                return True
        return False

    def __eq__(self, other):
        return self._id == other._id

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __repr__(self):
        return str(self._length)


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

    def init(self):
        self._ships = self.create_ships()

    def create_ships(self):
        empty_coords = list(sum([[(x, y) for y in range(self._size)] for x in range(self._size)], []))
        empty_ships = list(sum([[Ship(5 - x, tp=randint(1, 2)) for _ in range(x)] for x in range(1, 5)], []))
        placed_ships = []

        for ship in empty_ships:
            free_coords = copy(empty_coords)
            while free_coords:
                coord = free_coords.pop(randint(0, len(free_coords) - 1))
                ship.set_start_coords(*coord)
                if self.valid_ship_location(ship, placed_ships):
                    for c in ship.get_around_coords():
                        if c in empty_coords:
                            empty_coords.remove(c)
                    placed_ships.append(ship)
                    break
        return placed_ships if len(placed_ships) == 10 else self.create_ships()

    def get_ships(self):
        return self._ships

    def valid_ship_location(self, ship, other_ships):
        if (not ship.is_out_pole(self._size)) and \
                (not any([ship.is_collide(s) for s in other_ships if s != ship])):
            return True
        return False

    def move_ships(self, go=1):
        for ship in self._ships:
            if ship._is_move:
                go = choice((go, -go))
                for _ in '..':
                    go = -go
                    shadow_ship = copy(ship)
                    shadow_ship.move(go)
                    if self.valid_ship_location(shadow_ship, self._ships):
                        ship.move(go)
                        break

    def show(self):
        for col in self.get_pole():
            print(*col)
        print()

    def get_pole(self):
        ships_coords = []
        for ship in self._ships:
            for coord in ship.get_coords():
                ships_coords.append(coord)
        return tuple(
            [tuple([1 if (x, y) in ships_coords else 0 for y in range(self._size)]) for x in range(self._size)])
