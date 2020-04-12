from trackManager import TrackManager
from mover import Mover

import pygame


class Game:

    def __init__(self):
        self.track_m = TrackManager()
        self.agent = Mover(pygame.math.Vector2(200, 200), 0)
        self.game_started = False

    def start(self):
        self.agent.__init__(self.track_m.active_track.start_pos, 0)
        self.track_m.active_track.start()
        self.game_started = True

    def update(self):
        if self.game_started:
            self.agent.update()
            if self.track_m.active_track.crossed_active_checkpoint(self.agent.prev_pos, self.agent.pos):
                self.track_m.active_track.next_checkpoint()
