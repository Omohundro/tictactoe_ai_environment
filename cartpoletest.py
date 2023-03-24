# -*- coding: utf-8 -*-
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import set_global_seeds, make_vec_env

from stable_baselines import PPO2
from stable_baselines import A2C
from stable_baselines import ACER
from TicTacToeEnvironment import TicTacToeEnvironment as tictactoe
from stable_baselines.common.vec_env import SubprocVecEnv
import time
import gym
import numpy as np


env = make_vec_env(tictactoe, n_envs=16)
#env = tictactoe()

# multiprocess environment

model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log="./logs")
model.learn(total_timesteps=2500000, tb_log_name="tictactoe_ppo2")
    
model.save("ppo2_tictactoe")

del model # remove to demonstrate saving and loading

model = PPO2.load("ppo2_tictactoe")

# Enjoy trained agent
obs = env.reset()
for i in range(1000):
    env.envs[0].render()
    time.sleep(1)
    action, _states = model.predict(obs, deterministic=True)
    #print(action)
   # print(action[0])
    obs, rewards, dones, info = env.step(action)
    
    if dones[0]:
        env.envs[0].render(board = info[0]['terminal_observation'])
        time.sleep(1)
    #print(rewards[0])
    # if dones[0]:
        
    #     break

obs = env.reset()
for i in range(9):
    env.envs[0].render()
    time.sleep(1)
    obs, rewards, dones, info = env.step([8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

env.close()


