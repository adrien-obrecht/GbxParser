import GameIDs


class Array:
    def __init__(self):
        self.size = 0
        self.data = []

    def add(self, other):
        self.data.append(other)
        self.size += 1

    def __eq__(self, other):
        return self.data == other.data


class Chunk:
    def __init__(self):
        self.id = None
        self.data = {}
        self.depth = 0

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __eq__(self, other):
        return self.data == other.data and self.id == other.id

    def keys(self):
        return self.data.keys()

    def __repr__(self):
        def rprint(dico, depth):
            s = ""
            for v in dico.keys():
                if isinstance(dico[v], Chunk):
                    s += "| " * depth + "\n"
                    s += "| " * depth + f"{dico[v].id}: \n"
                    s += rprint(dico[v], depth + 1)
                elif isinstance(dico[v], Node):
                    dico[v].depth = self.depth + 1
                    s += str(dico[v])
                else:
                    s += "| " * depth + f"{v} : {dico[v]} \n"
            return s
        return "| " * self.depth + f"Chunk {self.id}: \n" + rprint(self.data, self.depth + 1)

    def __sub__(self, other):
        c = Chunk()

        c.id = self.id if (self.id == other.id) else (self.id, other.id)
        for el in self.data:
            if el not in other.data or self.data[el] != other.data[el]:
                c.data[el] = self.data[el]
        return c

    def count_node(self):
        r = 0
        for el in self.data.values():
            if isinstance(el, Node) and el.id is not None:
                r += el.count_node()
        return r


class List:
    def __init__(self):
        self.size = 0
        self.data = []

    def add(self, other):
        self.data.append(other)
        self.size += 1

    def __eq__(self, other):
        return self.data == other.data

    def __iter__(self):
        for v in self.data:
            yield v


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


class File:
    def __init__(self):
        self.version = -1
        self.checksum = -1
        self.path = ''
        self.locator_url = ''

    def __repr__(self):
        return f"{self.path} {self.locator_url}"


class Color:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def __repr__(self):
        return f"Color ({self.r}, {self.g}, {self.b})"


class Node:
    def __init__(self):
        self.id = None
        self.data = {}
        self.chunk_list = []
        self.depth = 0

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __eq__(self, other):
        return self.data == other.data and self.id == other.id

    def __repr__(self):
        f = ""
        for chunk in self.chunk_list:
            chunk.depth = self.depth + 1
            f += f"{chunk}"
        return "| " * self.depth + f"Node {self.id}: \n" + f

    def keys(self):
        return self.data.keys()

    def __sub__(self, other):
        n = Node()

        n.id = self.id if (self.id == other.id) else (self.id, other.id)
        for i in range(len(self.chunk_list)):
            n.chunk_list.append(self.chunk_list[i] - other.chunk_list[i])
        return n

    def count_node(self):
        return 1 + sum(c.count_node() for c in self.chunk_list)

