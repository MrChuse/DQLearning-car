class Track:

    def __init__(self, width, vertices=[]):
        self.vertices = vertices
        self.width = width
        self.magnet_threshold = 400

    def add_vertex(self, pos):
        for vertex in self.vertices:
            if (vertex - pos).length_squared() < self.magnet_threshold:
                pos = vertex
                break
        self.vertices.append(pos)
