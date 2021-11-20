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
