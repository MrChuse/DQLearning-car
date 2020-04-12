import pygame.math as math


class Track:

    def __init__(self, width, vertices=None, checkpoints=None, start=None):
        self.vertices = vertices if vertices is not None else []
        self.checkpoints = checkpoints if checkpoints is not None else []
        self.start = start if start is None else math.Vector2()
        self.width = width
        self.magnet_threshold = 400

    def add_vertex(self, pos):
        if len(self.vertices) == 0:
            self.start = pos
        for vertex in self.vertices:
            if (vertex - pos).length_squared() < self.magnet_threshold:
                pos = vertex
                break
        self.vertices.append(pos)

    def add_checkpoint(self, pos1, pos2):
        self.checkpoints.append((pos1, pos2))

    def set_start(self, pos):
        self.start = pos
