#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 22:15:09 2019

@author: chaninlaohaphan
"""

class Player():
        
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        
    def set_game_piece(self, piece, color):
        self.piece = piece
        self.color = color
        
        
class MachinePlayer(Player):
    
    def __init__(self):
        self.name = type(self).__name__
        self.playerType = 'machine'
        
    def make_move(self, board):
        raise NotImplementedError('Machine player must implement this method.')
