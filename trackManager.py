import pickle

from track import Track


class TrackManager:
    def __init__(self):
        self.tracks = []
        self.active_track = Track()

    def save_active_track(self):
        with open(f'track_{len(self.tracks)}.pickle', 'wb') as f_out:
            pickle.dump(self.active_track, f_out)

    def load_to_active_track(self, f_name):
        with open(f_name, 'rb') as f_in:
            self.active_track = pickle.load(f_in)

    def new_track(self):
        self.tracks.append(self.active_track)
        self.active_track = Track(50)

    def delete_track(self, number):
        self.tracks.pop(number)

    def clear_active_track(self):
        self.active_track.vertices = [[]]
        self.active_track.current_cycle = 0
        self.active_track.checkpoints = []
        self.active_track.start_pos = None
        self.active_track.active_checkpoint = None
