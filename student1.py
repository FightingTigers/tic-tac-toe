#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 07:13:26 2019

@author: chaninlaohaphan
"""

from player import MachinePlayer
import random
            


class RandomBot(MachinePlayer):
    
    def make_move(self, board):
        x = random.randrange(3)
        y = random.randrange(3)
        while board[x][y] != ' ':
            x = random.randrange(3)
            y = random.randrange(3)
        return (x,y)
    
    
class ThinkBot(MachinePlayer):
    
    def make_move(self, board):
        points = self.get_winning_positions(board, self.check_win)
        if len(points) > 0:
            return points[random.randrange(len(points))]
        points = self.get_winning_positions(board, self.check_lose)
        if len(points) > 0:
            return points[random.randrange(len(points))]
        points = self.get_playable_positions(board)
        if len(points) > 0:
            return points[random.randrange(len(points))]
        return None
    
    def get_winning_positions(self, board, check_win):
        result = []
        for i in range(3):
            if check_win(board[i]):
                result.append((i, board[i].index(' ')))
            column = [board[0][i], board[1][i], board[2][i]]
            if check_win(column):
                result.append((column.index(' '), i))
        diagonal = [board[0][0], board[1][1], board[2][2]]
        if check_win(diagonal):
            x = diagonal.index(' ')
            result.append((x, x))
        diagonal = [board[2][0], board[1][1], board[0][2]]
        if check_win(diagonal):
            x = diagonal.index(' ')
            result.append((2-x,x))
        return result
        
    def check_win(self, row):
        return row.count(self.piece) == 2 and row.count(' ') == 1
        
    def check_lose(self, row):
        return row.count(self.piece) == 0 and row.count(' ') == 1
        
    def get_playable_positions(self, board):
        return [(row_index, col_index) for row_index in range(3) 
                for col_index in range(3) if board[row_index][col_index] == ' ']
    

        
