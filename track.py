import pygame.math as math


class Track:

    def __init__(self, width, vertices=None, checkpoints=None, start=None):
        self.vertices = vertices if vertices is not None else []
        self.checkpoints = checkpoints if checkpoints is not None else []
        self.start_pos = start if start is None else math.Vector2()
        self.width = width
        self.magnet_threshold = 400

        self.active_checkpoint = None
        self.counter = 0

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
        self.counter = 0

    def next_checkpoint(self):
        self.counter = (self.counter + 1) % len(self.checkpoints)
        self.active_checkpoint = self.checkpoints[self.counter]

    def crossed_active_checkpoint(self, pos1, pos2):
        if pos1.x > pos2.x:
            pos1, pos2 = pos2, pos1
        x1, x2, x3, x4 = pos1.x, pos2.x, self.active_checkpoint[0].x, self.active_checkpoint[1].x
        y1, y2, y3, y4 = pos1.y, pos2.y, self.active_checkpoint[0].y, self.active_checkpoint[1].y
        # count k1
        if x2 == x1:
            # todo: check when vertical
            return False
        a = (y2 - y3 + (x3-x1) * (y2-y1) / (x2-x1))
        b = (y4 - y3 - (x4-x3) * (y2-y1) / (x2-x1))
        print(a, b)
        if b == 0:
            # todo: check when parallel
            return False
        t2 = a / b
        t1 = (x3 - x1 + t2 * (x4-x3)) / (x2 - x1)
        ans = 0 <= t1 <= 1 and 0 <= t2 <= 1
        return ans
        # return t1, t2


