import pygame.math as math


class Mover:
    def __init__(self, pos, direction):
        self.pos = math.Vector2(pos)
        self.dir = direction

        self.vel = math.Vector2()
        self.a_vel = 0

        self.acc = math.Vector2()
        self.a_acc = 0

        self.prev_pos = math.Vector2(pos)
        self.prev_dir = direction

    def update(self):
        self.prev_pos.update(self.pos)
        self.prev_dir = self.dir

        self.pos += self.vel
        self.dir += self.a_vel

        self.vel += self.acc
        self.a_vel += self.a_acc

        self.acc.update(0, 0)
        self.a_acc = 0

    def add_force(self, force, rotation):
        self.acc += force
        self.a_acc += rotation
