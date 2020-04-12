from trackManager import TrackManager
from mover import Mover

import pygame


class Game:

    def __init__(self):
        self.track_m = TrackManager()
        self.agent = Mover(pygame.math.Vector2(200, 200), 0)

    def start(self):
        self.agent.__init__(self.track_m.active_track.start_pos, 0)
        self.track_m.active_track.start()
