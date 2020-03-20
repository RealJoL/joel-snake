import snake
import matplotlib.pyplot as plt


def render(game):
    plt.rcParams['keymap.save'].remove('s')
    fig, ax = plt.subplots(1, 1)
    ax.spy(game.get_playing_field(), markersize=12)
    fig.suptitle("Snake! Your score: " + str(game.get_score()), fontsize=8)

    plt.ion()
    plt.show()

    while not game.is_game_lost():
        fig.suptitle("Snake! Your score: " + str(game.get_score()), fontsize=8)
        plt.cla()
        ax.spy(game.get_playing_field(), markersize=12)
        plt.draw()
        plt.pause(0.001)
