import csv


class Track:
    def __init__(self, id, valence, arousal):
        self.id = id
        self.valence = valence
        self.arousal = arousal


class Utils:
    @staticmethod
    def read_data(path):

        tracks = list()
        file = open(path, 'r')
        csv_reader = csv.reader(file, delimiter=',')
        data_list = list(csv_reader)

        for i in data_list:
            tracks.append(Track(i[0], i[1], i[2]))

        return tracks

    # find nearest song id to propose
    # should return list of [valence, arousal]
    @staticmethod
    def find_nearest(valence, arousal, tracks):

        min_distance = 100000
        nearest_track = Track(1001, 10, 10)

        for track in tracks:
            valence_diff = (float(valence) - float(track.valence))
            arousal_diff = (float(arousal) - float(track.arousal))

            distance = valence_diff*valence_diff + arousal_diff*arousal_diff
            if distance < min_distance:
                min_distance = distance
                nearest_track = track

        return nearest_track
