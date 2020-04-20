import pygame.math as math


class Track:

    def __init__(self, vertices=None, checkpoints=None, start=None):
        self.vertices = vertices if vertices is not None else [[]]
        self.checkpoints = checkpoints if checkpoints is not None else []
        self.start_pos = start if start is None else math.Vector2()
        self.magnet_threshold = 400

        self.active_checkpoint = None
        self.counter = 0
        self.current_cycle = 0

    def add_vertex(self, pos):
        for cycle in self.vertices:
            for vertex in cycle:
                if (vertex - pos).length_squared() < self.magnet_threshold:
                    pos = math.Vector2(vertex)
                    break
        self.vertices[self.current_cycle].append(pos)

    def add_cycle(self):
        self.vertices.append([])
        self.current_cycle = len(self.vertices) - 1

    def move_current_cycle(self):
        self.current_cycle = (self.current_cycle + 1) % len(self.vertices)

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

    def check_intersection(self, pos11, pos12, pos21, pos22):
        if pos11.x > pos12.x:
            pos11, pos12 = pos12, pos11
        if pos21.x > pos22.x:
            pos21, pos22 = pos22, pos21
        x1, x2, x3, x4 = pos11.x, pos12.x, pos21.x, pos22.x
        y1, y2, y3, y4 = pos11.y, pos12.y, pos21.y, pos22.y
        # count k1
        if x2 == x1:
            # todo: check when vertical
            return False
        a = (y2 - y3 + (x3-x1) * (y2-y1) / (x2-x1))
        b = (y4 - y3 - (x4-x3) * (y2-y1) / (x2-x1))
        if b == 0:
            # todo: check when parallel
            return False
        t2 = a / b
        t1 = (x3 - x1 + t2 * (x4-x3)) / (x2 - x1)
        ans = 0 <= t1 <= 1 and 0 <= t2 <= 1
        return ans
        # return t1, t2


