# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:09:17 2021

@author: Rilin
"""

import gym
from gym import spaces
import numpy as np
from random import randrange
import math

BOARD_SIZE = 9

class TicTacToeEnvironment(gym.Env):
    
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE,), dtype=int)
        # 9 Actions, model will pick from numbers 0-8 represnting a position on the board
        self.action_space = spaces.Discrete(BOARD_SIZE)
        # Observation space (1, 9), meaning an array of 1 row and 9 columns - representing the board
        # O will be classified as -1, X will be classified as 1 and an empty spot will be classified as 0
        self.observation_space = spaces.Box(low=-1, high=1,
                                        shape=(1, BOARD_SIZE), dtype=np.float32)
        
        self.viewer = None
        
    def reset(self):
        #print("RESETTING")
        self.board = np.zeros((BOARD_SIZE,), dtype=int) 
        return self.board
    
    def step(self, action):
        
        #print("Selected action %s " % (action))
        
        if self.board[action] != 0:
            #print("Selected a spot that was taken, reselecting")
            board_copy = self.board.copy()
            return (self.board, -1, False, {})
        # Set the AI's chosen position on the board
        self.board[action] = 1
        
        reward, done = self.check_for_end()
        
        if done:
            return (self.board, reward, done, {})
        
        # The CPU choses a random spot on the board
       # print("CPU Choosing random position")
        chosen_position = randrange(9)       
        while self.board[chosen_position] != 0:
            chosen_position = randrange(9)
            #print("CHOOSING POSITION")
        
        self.board[chosen_position] = -1
       # print("CPU chose position %s" % (chosen_position))
        
        reward, done = self.check_for_end()
        
        board_copy = self.board.copy()
        
       # print(done)
        return (self.board, reward, done, {})
    
    def check_for_end(self):
        reward = 0
        done = False
        # Check rows for winners
        if self.board[0] == self.board[1] and self.board[1] == self.board[2]:
            if self.board[0] != 0:
                if self.board[0] == 1:
                    #print("0-1-2")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
             
        if self.board[3] == self.board[4] and self.board[4] == self.board[5]:
            if self.board[3] != 0:
                if self.board[3] == 1:
                    #print("3-4-5")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
                 
        if self.board[6] == self.board[7] and self.board[7] == self.board[8]:
            if self.board[6] != 0:
                if self.board[6] == 1:
                    #print("6-7-8")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
        
        # Check columns for winners
        
        if self.board[0] == self.board[3] and self.board[3] == self.board[6]:
            if self.board[0] != 0:
                if self.board[0] == 1:
                    #print("0-3-6")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
                 
                 
        if self.board[1] == self.board[4] and self.board[4] == self.board[7]:
            if self.board[1] != 0:
                if self.board[1] == 1:
                   # print("1-4-7 (%s)" % (self.board))
                    reward = 1
                else:
                    reward = -1
                    
                done = True
        
        
        if self.board[2] == self.board[5] and self.board[5] == self.board[8]:
            if self.board[2] != 0:
                if self.board[2] == 1:
                    #print("2-5-8")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
                 
    
        # Check diagoal for winners
        
        if self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            if self.board[0] != 0:
                if self.board[0] == 1:
                    #print("0-4-8")
                    reward = 1
                else:
                    reward = -1
                    
                done = True
        
        
        if self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            if self.board[2] != 0:
                if self.board[2] == 1:
                    reward = 1
                    #print("2-4-6")
                else:
                    reward = -1
                    
                done = True
        
        # if reward == 1:
        #     print("WE WON!")
        # elif reward == -1:
        #     print("WE LOST")
            
        # Check for draw
        if not done:
            is_space_left = False
            for i in range(len(self.board)):
                if self.board[i] == 0:
                    is_space_left = True
                    break
            if not is_space_left:
                done = True
                #print("ITS A DRAW")
                
        return(reward, done)
    
    def render(self, mode='human', board = None):
        
        if board is None:
            board_to_render = self.board
        else:
            board_to_render = board
            print("Rendering terminal observation: %s" % (board))
            
        #print(self.board)
        screen_width = 600
        screen_height = 600
        #print(self.board)

        #world_width = self.x_threshold * 2
        #scale = screen_width/world_width
        from gym.envs.classic_control import rendering
         
        if self.viewer is None:
            self.viewer = rendering.Viewer(screen_width, screen_height)
            l, r, t, b = 200, 205, 0, 600
            left_column = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.viewer.add_geom(left_column)
            l, r, t, b = 400, 405, 0, 600
            right_column = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.viewer.add_geom(right_column)
            l, r, t, b = 0, 600, 200, 205
            top_row = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.viewer.add_geom(top_row)
            l, r, t, b = 0, 600, 400, 405
            bottom_row = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.viewer.add_geom(bottom_row)
            
        
        for i in range(len(board_to_render)):
            symbol = board_to_render[i]
            if symbol == 1:
                l, r, t, b = 100 + ( (i%3)*200) - 25, 100 + ( (i%3)*200) + 25, 500  - (math.floor((i/3))*200) - 2, 500  - (math.floor((i/3))*200) + 2
                line = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
                self.viewer.add_onetime(line)
            elif symbol == -1:
                l, r, t, b = 100 + ( (i%3)*200) - 2, 100 + ( (i%3)*200) + 2, 500  - (math.floor((i/3))*200) - 25, 500  - (math.floor((i/3))*200) + 25
                line = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
                self.viewer.add_onetime(line)
                
        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
            
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
        
        
        