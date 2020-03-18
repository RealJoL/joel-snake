from pynput import keyboard
import snake


class Listener:
    def __init__(self, game):
        self.cur_game = game
        self.inputs = {'d': 3, 's': 0, 'a': 1, 'w': 2}
        self.start_it_up()

    def start_it_up(self):
        # Collect until released
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        if self.cur_game.is_game_lost():
            self.on_release(-1)  # Fix da keine Ahnung wie thread beenden
        try:
            if key.char in self.inputs:
                print("set direction to " + key.char)
                self.cur_game.set_directions(self.inputs[key.char])
        except AttributeError:
            print("hard pass bro")
            pass

    def on_release(self, key):
        if self.cur_game.is_game_lost() or key == -1 or key == keyboard.Key.esc:
            # Stop listener
            return False
