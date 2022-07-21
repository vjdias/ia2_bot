"""arm controller."""

from SteveShoots import BotController
import numpy
import time
import numpy as np
from random import randrange
from enum import Enum
from tqdm import trange

import random
from controller import Supervisor
random.seed(42)

from tiles3 import tiles, IHT

DISCOUNT = 0.99  # gamma
EXPLORE_RATE = 0.1  # epsilon

EPISODES = (50, 10)
MAX_ITER = 250

maxSize = 8192
iht = IHT(maxSize)
numTilings = 16
stepSize = 0.5/numTilings

weights = np.zeros(shape=maxSize)

# Cria o tiles
def mytiles(X, tile_dim=5.0, min_x=-4., max_x=4.):
    scaleFactor = tile_dim / (max_x - min_x)
    X[0] *= tile_dim/(2*2.4)
    X[1] *= tile_dim/(2*5)
    X[2] *= tile_dim/(2*0.2)
    return tiles(iht, numTilings, X)


def v_hat(X):
    return weights[mytiles(X)].sum()


timestep = 1 
time_duration = 1000
time_after_shoot = 0

srobot = Supervisor()   
bot = BotController(srobot,timestep)

total_moves = 5
direction = [-1, 1]
moviment  = [0, 27, 45, 90]
shoot     = [0, 1]

list_possibilities = numpy.array(numpy.meshgrid([-1, 1], [0, 10], [-1, 1], [0, 10])).T.reshape(-1,4)
indice = range(len(list_possibilities))

print("ln")


if __name__ == "__main__":
    episodes_loop = trange(EPISODES[0])
    print("ln")
    for i_episode in episodes_loop:
        observation = randrange(len(list_possibilities))
        print("ln")

        for i in range(EPISODES[1]):
            time_after_shoot = 0
            while (time_duration - time_after_shoot) > 0:
                curr_state = bot.obs()
                print("ln")
                if np.random.uniform() < EXPLORE_RATE:
                    # Escolhe ação aleatoriamente
                    action = randrange(len(list_possibilities))
                else:                                       
                    action = 0
                    for a in range(len(list_possibilities)):
                        b = v_hat(np.concatenate((curr_state,[a])))
                        if b > action:
                            action = b
                             
                    
                    
                # Aplica a ação
                print(action)
                observation = bot.action(list_possibilities[action])
                time_after_shoot = time.time()
                next_state = observation()
                # Salva o estado
                state_tiles = mytiles(np.concatenate([curr_state, [action]]))
                v_hat_next = np.max(
                    np.array(
                        [
                            v_hat(np.concatenate(
                                [next_state, [a]])) for a in range(2)
                        ]
                    )
                )
                
                # Atualize o valor Q
                weights[state_tiles] += stepSize * (
                    reward + DISCOUNT * v_hat_next - v_hat(
                        np.concatenate([curr_state, [action]])
                    )
                )
    

                if done:
                    break







# Enter here exit cleanup code.
