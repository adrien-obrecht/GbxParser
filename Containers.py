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
                if isinstance(dico[v], (Chunk, Node)) and len(str(dico[v])) < 200000:
                    s += "| " * depth + "\n"
                    s += "| " * depth + f"{dico[v].id}: \n"
                    s += rprint(dico[v], depth + 1)
                else:
                    s += "| " * depth + f"{v} : {dico[v]} \n"
            return s
        return f"Node {self.id}: \n" + rprint(self.data, self.depth + 1)


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


class Node:
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

    def __repr__(self):
        def rprint(dico, depth):
            s = ""
            for v in dico.keys():
                if isinstance(dico[v], (Chunk, Node)) and len(str(dico[v])) < 200000:
                    s += "| " * depth + "\n"
                    s += "| " * depth + f"{dico[v].id}: \n"
                    s += rprint(dico[v], depth + 1)
                else:
                    s += "| " * depth + f"{v} : {dico[v]} \n"
            return s
        return f"Node {self.id}: \n" + rprint(self.data, self.depth + 1)

    def print_diff(self, other, path=""):
        if self.id != other.id:
            print("This nodes aren't the same!")
        else:
            for e in self.keys():
                if e not in other.keys():
                    print(f"{e} in {path}")
                    print(f"This value is not in copy : {e}")
                    print()
                elif isinstance(self[e], Node):
                    self[e].print_diff(other[e], path+str(e))
                elif self[e] != other[e]:
                    print(f"{e} in {path}")
                    print(self[e])
                    print(other[e])
                    print()

    def keys(self):
        return self.data.keys()


