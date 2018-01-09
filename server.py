#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from tensorforce.agents import PPOAgent
import json
from data import Track, Utils
from collections import namedtuple

# Agent specification
agent = PPOAgent(
    states_spec=dict(type='float', shape=(4,)),
    actions_spec=dict(shape=(2,), type='float', min_value=-1, max_value=1),
    network_spec=[
        dict(type='dense', size=64),
        dict(type='dense', size=64),

    ],

    batch_size=100,
)


# HTTPRequestHandler class
class PPOMusicServer(BaseHTTPRequestHandler):

    # user Valence/Arousal, song (agent) state with Valence/Arousal
    state = [0, 0, 0, 0]
    tracks = Utils.read_data("/home/wigdis/praca_inz/emotion_in_music/annotations/data.csv")


    # GET - latest song, for starting and closing mobile app purpose
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        nearest_song = Utils.find_nearest(PPOMusicServer.state[2], PPOMusicServer.state[3], self.tracks)
        response = '{ "id": "'+str(nearest_song.id)+'" }'
        self.wfile.write(response.encode("utf-8"))
        return


    def do_POST(self):
        # json deserialization
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        # print(data.reward)
        # print(data.valence)
        # print(data.arousal)

        # user mood set
        PPOMusicServer.state[0] = data.valence
        PPOMusicServer.state[1] = data.arousal

        agent.observe(reward=data.reward, terminal=False)
        action = agent.act(PPOMusicServer.state)

        valence = action[0]
        arousal = action[1]
        nearest_song = Utils.find_nearest(valence, arousal, self.tracks)

        # state setting - nearest song
        PPOMusicServer.state[2] = nearest_song.valence
        PPOMusicServer.state[3] = nearest_song.arousal

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = '{ "id": "'+str(nearest_song.id)+'" }'
        self.wfile.write(response.encode("utf-8"))

        return


def run():
    print('starting server...')

    # Server settings
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, PPOMusicServer)

    print('running server...')
    # Otherwise, there is no proper action and state space
    action = agent.act(PPOMusicServer.state)
    valence = action[0]
    arousal = action[1]
    nearest_song = Utils.find_nearest(valence, arousal, PPOMusicServer.tracks)
    PPOMusicServer.state[2] = nearest_song.valence
    PPOMusicServer.state[3] = nearest_song.arousal

    httpd.serve_forever()

run()
