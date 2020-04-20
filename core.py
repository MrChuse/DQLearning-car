from trackManager import TrackManager
from mover import Mover

import pygame


class Game:

    def __init__(self, num_actions=8):
        self.track_m = TrackManager()
        self.agent = Mover(pygame.math.Vector2(200, 200), 0)
        self.game_started = False
        self.num_actions = num_actions
        self.tick = None

    def start(self):
        self.agent.__init__(self.track_m.active_track.start_pos, 0)
        self.track_m.active_track.start()
        self.game_started = True
        self.tick = 0

    def update(self, action):
        self.tick += 1
        terminal = self.tick >= 2500

        angle = action * 360 / self.num_actions
        force = pygame.math.Vector2()
        force.from_polar((1, angle))

        if force.length() > 0:
            force_ = force.normalize()
            force_.scale_to_length(0.01)
            self.agent.add_force(force_, 0)
        if self.game_started:
            self.agent.update()
            for cycle in self.track_m.active_track.vertices:
                for start, end in zip(cycle[:-1], cycle[1:]):
                    if self.track_m.active_track.check_intersection(self.agent.prev_pos, self.agent.pos, start, end):
                        return -100, True
            if self.track_m.active_track.check_intersection(self.agent.prev_pos,
                                                            self.agent.pos,
                                                            self.track_m.active_track.active_checkpoint[0],
                                                            self.track_m.active_track.active_checkpoint[1]):
                self.track_m.active_track.next_checkpoint()
                return 100, terminal

        return -1, terminal

    def get_state(self):
        return self.track_m.active_track.active_checkpoint[0] - self.agent.pos, self.track_m.active_track.active_checkpoint[1] - self.agent.pos
