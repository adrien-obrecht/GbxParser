from typing import Union

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
        seen = set()

        def dd(depth: int) -> str:
            s = ""
            for i in range(depth):
                if i & 1:
                    s += "   "
                else:
                    s += "|  "
            return s

        def rprint(cont: Union[Node, Chunk], depth: int, name: str = None) -> str:
            s = ""
            if isinstance(cont, Chunk):
                s += dd(depth) + f"{cont.id}: \n"
                for v in cont.data.keys():
                    s += rprint(cont.data[v], depth + 1, name=v)
            elif isinstance(cont, Node):
                s += dd(depth) + f"{cont.id} : {name}"
                if cont not in seen:
                    seen.add(cont)
                    s += "\n"
                    for c in cont.chunk_list:
                        s += rprint(c, depth + 1)
                else:
                    s += "(already printed)\n"
                s += dd(depth) + "\n"
            else:
                s += dd(depth) + f"{name} : {cont} \n"
            return s

        return rprint(self, 0)

    def __sub__(self, other):
        c = Chunk()

        c.id = self.id if (self.id == other.id) else (self.id, other.id)
        for el in self.data:
            if el not in other.data or self.data[el] != other.data[el]:
                c.data[el] = self.data[el]
        return c


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
        self.chunk_list = []
        self.depth = 0

    # TODO: This was implemented to use noderef, not super happy with it
    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def __repr__(self):
        seen = set()

        def dd(depth: int) -> str:
            s = ""
            for i in range(depth):
                if i & 1:
                    s += "   "
                else:
                    s += "|  "
            return s

        def rprint(cont: Union[Node, Chunk], depth: int, name: str = None) -> str:
            s = ""
            if isinstance(cont, Chunk):
                s += dd(depth) + f"{cont.id}: \n"
                for v in cont.data.keys():
                    s += rprint(cont.data[v], depth + 1, name=v)
            elif isinstance(cont, Node):
                s += dd(depth) + "\n" + dd(depth) + f"{cont.id} : {name}"
                if cont not in seen:
                    seen.add(cont)
                    s += "\n"
                    for c in cont.chunk_list:
                        s += rprint(c, depth + 1)
                else:
                    s += "(already printed)\n"
            else:
                s += dd(depth) + f"{name} : {cont} \n"
            return s

        return rprint(self, 0)

    def keys(self):
        return self.data.keys()

    def __sub__(self, other):
        n = Node()

        n.id = self.id if (self.id == other.id) else (self.id, other.id)
        for i in range(len(self.chunk_list)):
            n.chunk_list.append(self.chunk_list[i] - other.chunk_list[i])
        return n

    def count_node(self):
        seen = set()

        def rcount(cont: Union[Node, Chunk]) -> int:
            s = 0
            if isinstance(cont, Chunk):
                for v in cont.data.keys():
                    s += rcount(cont.data[v])
            elif isinstance(cont, Node):
                if id(cont) not in seen:
                    seen.add(id(cont))
                    s += 1
                    for c in cont.chunk_list:
                        s += rcount(c)
            return s

        return rcount(self)

