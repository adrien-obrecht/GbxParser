class Gbx:
    def __init__(self):
        self.id = None
        self.header_chunk_list = []
        self.main_node = None
        self.raw_data = None

    def __repr__(self):
        f = f" Gbx : {self.id}\n\n"

        if self.header_chunk_list:
            f += "Header chunks : \n\n"
            for chunk in self.header_chunk_list:
                f += str(chunk) + "\n"

        f += str(self.main_node)

        return f

    def __sub__(self, other):
        g = Gbx()
        g.id = self.id if (self.id == other.id) else (self.id, other.id)
        for i in range(len(self.header_chunk_list)):
            g.header_chunk_list.append(self.header_chunk_list[i] - other.header_chunk_list[i])
        g.main_node = self.main_node - other.main_node
        return g
