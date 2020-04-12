import pygame.math as math


class Track:

    def __init__(self, width, vertices=None, checkpoints=None, start=None):
        self.vertices = vertices if vertices is not None else []
        self.checkpoints = checkpoints if checkpoints is not None else []
        self.start_pos = start if start is None else math.Vector2()
        self.width = width
        self.magnet_threshold = 400

        self.active_checkpoint = None

    def add_vertex(self, pos):
        if len(self.vertices) == 0:
            self.start_pos = pos
        for vertex in self.vertices:
            if (vertex - pos).length_squared() < self.magnet_threshold:
                pos = vertex
                break
        self.vertices.append(pos)

    def add_checkpoint(self, pos1, pos2):
        if pos1.x > pos2.x:
            pos1, pos2 = pos2, pos1
        if len(self.vertices) == 0:
            self.active_checkpoint = (pos1, pos2)
        self.checkpoints.append((pos1, pos2))

    def set_start(self, pos):
        self.start_pos = pos

    def start(self):
        self.active_checkpoint = self.checkpoints[0]



