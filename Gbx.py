class Gbx:
    def __init__(self):
        self.id = None
        self.header_chunk_list = []
        self.node_list = []

    def __repr__(self):
        f = f" Gbx : {self.id}\n\n"

        if self.header_chunk_list:
            f += "Header chunks : \n\n"
            for chunk in self.header_chunk_list:
                f += str(chunk) + "\n"

        if self.node_list:
            f += "Nodes : \n\n"
            for node in self.node_list:
                f += str(node) + "\n"

        return f

    def __sub__(self, other):
        g = Gbx()
        g.id = self.id if (self.id == other.id) else (self.id, other.id)
        for i in range(len(self.header_chunk_list)):
            g.header_chunk_list.append(self.header_chunk_list[i] - other.header_chunk_list[i])
        g.node_list = [self.node_list[0] - other.node_list[0]]
        return g
