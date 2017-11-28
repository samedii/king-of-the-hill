
import numpy as np
import matplotlib.pyplot as plt
import map
import game
import player
import visualize

def main():

    m = map.HomelyHill()

    def play_map(player, game_map):
        g = game.Game(game_map)
        player.play(g)
        return g
    
    players = [player.Human(), player.NaturalSelection(), player.NaturalEvolutionSGD(), player.FiniteDifferences(), player.ScipyOptimizer('BFGS'), player.ScipyOptimizer('Powell'), player.ScipyOptimizer('Nelder-Mead'), player.ScipyOptimizer('CG'), player.ScipyOptimizer('COBYLA')]
    games = [play_map(player, m) for player in players]

    v = visualize.Visualize(players, games, m)
    v.show(n_evaluations=1)

main()