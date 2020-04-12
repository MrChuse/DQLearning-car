from trackManager import TrackManager
from mover import Mover

import pygame


class Game:

    def __init__(self):
        self.track_m = TrackManager()
        self.agent = Mover(pygame.math.Vector2(200, 200), 0)
