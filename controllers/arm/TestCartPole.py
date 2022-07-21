# -*- coding: utf-8 -*-
"""
Created on Wed May 11 00:27:22 2022

@author: Clara
"""

import gym
import numpy as np
import random
from IPython.display import clear_output

x_discrete_angle = np.arange(-0.418 ,0.418 ,0.01)
y_discrete_angular_velocity  = np.arange(-4, 4, 0.1)

# Inicialização com a tabela de valores Q
t = np.load('cartpole_data.npz')
q_table = t['arr_0']

env = gym.make('CartPole-v1').env
env.reset()
state = env.reset()

action = np.argmax(q_table[0][0])

count = 200
for r in range(1000):
    env.render()
    next_state, reward, done, info = env.step(action)
    
    y_id = np.digitize(next_state[3], y_discrete_angular_velocity)
    x_id = np.digitize(next_state[2], x_discrete_angle)
    action = np.argmax(q_table[x_id][y_id]) # Escolhe ação com base no que já aprendeu
    print(x_discrete_angle[x_id], y_discrete_angular_velocity[y_id] ,action)
    
env.close()