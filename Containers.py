class Array:
    def __init__(self):
        self.size = 0
        self.data = []

    def add(self, other):
        self.data.append(other)
        self.size += 1

    def __eq__(self, other):
        return self.data == other.data


class List:
    def __init__(self):
        self.size = 0
        self.data = []

    def add(self, other):
        self.data.append(other)
        self.size += 1

    def __eq__(self, other):
        return self.data == other.data


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        return None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        return None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

