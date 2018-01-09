import csv
from statistics import median


def write_data():
    path_arousal = "/home/wigdis/praca_inz/emotion_in_music/annotations/arousal.csv"
    path_valence = "/home/wigdis/praca_inz/emotion_in_music/annotations/valence.csv"

    path_output = "/home/wigdis/praca_inz/emotion_in_music/annotations/data.csv"

    ar_file = open(path_arousal, 'r')
    val_file = open(path_valence, 'r')
    data_file = open(path_output, 'w')

    arousal_reader = csv.reader(ar_file, delimiter=',')
    valence_reader = csv.reader(val_file, delimiter=',')

    arousal_list = list(arousal_reader)
    valence_list = list(valence_reader)

    for i, _ in enumerate(arousal_list):
        if i == 0:
            continue

        id = arousal_list[i].pop(0)

        arousal_mean = median(arousal_list[i])
        valence_list[i].pop(0)

        valence_mean = median(valence_list[i])

        fieldnames = ['id', 'valence', 'arousal']
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writerow({'id': id, 'valence': valence_mean, 'arousal': arousal_mean})


write_data()
