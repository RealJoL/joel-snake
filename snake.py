import numpy as np
import queue
import on_a_plane
import matplotlib.pyplot as plt
from threading import Thread
import time
import listen_here_you


def get_directions(move):
    part = (move == 1 or move == 3)
    one4positive = (move == 0 or move == 3)
    return int(part), int(one4positive)


class Snake:
    def __init__(self):
        self.playing_field = np.zeros((20, 20))
        # 3 right, 0 down, 1 left, 2 up
        self.head = [10, 10]
        self.tail = [10, 10]
        self.current_move = 0
        self.game_lost = False
        self.last_input = queue.Queue()
        self.score_point = [21, 21]

    def start_game(self):
        self.playing_field[10, 10] = 1
        self.place_point()
        self.game_lost = False

        listen_t = Thread(target=self.listen_to_me, args=[])
        game_t = Thread(target=self.run_game, args=[])
        graph_t = Thread(target=on_a_plane.render, args=[self])

        listen_t.start()
        graph_t.start()
        game_t.start()
        listen_t.join()
        graph_t.join()
        game_t.join()
        print("Game finished")

    def is_game_lost(self):
        return self.game_lost

    def set_directions(self, direct):
        if abs(self.current_move - direct) == 2:
            return
        self.current_move = direct

    def get_playing_field(self):
        return self.playing_field

    def listen_to_me(self):
        listener = listen_here_you.Listener(self)

    def run_game(self):
        time.sleep(1)
        while not self.game_lost:
            time.sleep(0.3)
            part, one4pos = get_directions(self.current_move)
            if one4pos:
                print(self.head[part])
                self.head[part] += 1
            else:
                self.head[part] -= 1

            self.last_input.put(self.current_move)

            if self.head[0] > 19 or self.head[0] < 0 \
                    or self.head[1] > 19 or self.head[1] < 0 or \
                    self.playing_field[self.head[0], self.head[1]] == 1:
                self.game_lost = True
                break

            self.playing_field[self.head[0], self.head[1]] = 1

            if self.head == self.score_point:
                self.place_point()
                continue

            move2remove = self.last_input.get()
            self.playing_field[self.tail[0], self.tail[1]] = 0

            part, one4pos = get_directions(move2remove)
            if one4pos:
                self.tail[part] += 1
            else:
                self.tail[part] -= 1

    def place_point(self):
        self.score_point = [np.random.randint(0, 20), np.random.randint(0, 20)]
        while self.playing_field[self.score_point[0], self.score_point[1]]:
            self.score_point = [np.random.randint(0, 20), np.random.randint(0, 20)]
        print("New coordinates " + str(self.score_point))
        self.playing_field[self.score_point[0], self.score_point[1]] = 2
        print(self.playing_field)

