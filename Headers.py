class Vector3(object):
    """The Vector3 class represents a 3D vector, usually read directly from the GBX file."""

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        return None

    def __eq__(self, other):
        if isinstance(other, list):
            return self.x == other[0] and self.y == other[1] and self.z == other[2]

        return self.x == other.x and self.y == other.y and self.z == other.z

    def as_array(self):
        """Returns the vector as a list.

        Returns:
            the vector as a list made of 3 elements
        """
        return [self.x, self.y, self.z]

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


class Block:
    def __init__(self):
        self.position = [0, 0, 0]
        self.name = None
        self.flags = 0
        self.rotation = 0

    def __repr__(self):
        return f'{self.position} {self.name} \n'

    def __eq__(self, other):
        return self.name == other.name and self.position == other.position

    def __hash__(self):
        return hash((self.name, self.position[0], self.position[1], self.position[2]))


class Point:
    def __init__(self):
        self.positions = []
        self.color = (0, 0, 0)
        self.opacity = 1

    def __repr__(self):
        return f'{self.positions=} {self.color=} {self.opacity=} \n'
