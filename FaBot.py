#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:55:59 2019

@author: fa
"""

from student1 import ThinkBot
import random


class FaBot (ThinkBot):
    
    def make_move(self, board):
        points = self.get_winning_positions(board, self.check_win)
        if len(points) > 0:
            return points[random.randrange(len(points))]
        points = self.get_winning_positions(board, self.check_lose)
        if len(points) > 0:
            return points[random.randrange(len(points))]
        points = self.get_playable_positions(board)
        count = self.count_round(board)
        if len(points) > 0:
            if count == self.their_count(board):
                if count == 0:
                    return (2,2)
                if count == 1:
                    x,y = self.their_move(board)
                    if (x,y) == (1,1):
                        return (0,0)
                    if abs(x-y) == 1:
                        return (1, 1)
                    else:
                        return self.available_corner(board)
                else:
                    if board[1][1] == self.piece:
                        return self.available_side(board)
                    else:
                        return self.available_corner(board)
            if count < self.their_count(board):
                if board[1][1] == ' ':
                   return (1,1)
                if count == 1:
                    if self.taken_corner(board) and self.taken_side(board) != None:
                        x,y = self.taken_corner(board)
                        return (abs(x-2),abs(y-2))
                    if self.corner_pair(board) != None:
                        return self.corner_pair(board)
                    return self.full_side(board)
                if count == 2:
                    if self.taken_corner(board) == None:
                        x,y= self.our_side(board)
                        if x == 1:
                            return (0,y)
                        else:
                            return (x,0)
                    else:
                        return points[random.randrange(len(points))]
                else:
                    return points[random.randrange(len(points))]
        return None
    
    def count_round (self,board):
        return board[0].count(self.piece) + board[1].count(self.piece) + board[2].count(self.piece)
    
    def their_move (self,board):
        enemy = self.their_piece()
        for x in range(3): 
            for y in range(3):
                if board[x][y] == enemy:
                    return (x,y)
    
    def their_piece (self):
        if self.piece == 'O':
            return 'X'
        else:
            return 'O'
# any available corner        
    def available_corner (self, board):
        for x in [0,2]:
            for y in [0,2]:
                if board [x][y] == ' ':
                    return (x,y)
 #only for limited corners, use full_side instead       
    def available_side (self,board):
        if board[1][2] == " ":
            return (1,2)
        else:
            return (2,1)
#for order purposes        
    def their_count (self,board):
        enemy = self.their_piece()
        return board[0].count(enemy) + board[1].count(enemy) + board[2].count(enemy)
 
#complete side availability    
    def full_side (self, board):
        for i in [0,2]:
            if board[1][i] == ' ':
                return (1,i)
            if board[i][1] == ' ':
                return (i,1)

#any corner taken by enemy                
    def taken_corner (self, board):
        for x in [0,2]:
            for y in [0,2]:
                if board [x][y] == self.their_piece():
                    return (x,y)
        return None
 
#any side taken by enemy    
    def taken_side(self, board):
        for i in [0,2]:
            if board[1][i] == self.their_piece():
                return (1,i)
            if board[i][1] == self.their_piece():
                return (i,1)
        
        return None
    
#our piece on the side    
    def our_side (self,board):
        for i in [0,2]:
            if board[1][i] == self.piece:
                return (1,i)
            if board[i][1] == self.piece:
                return (i,1)
            
#sides @ 90 degrees angle
    def corner_pair(self,board):
        if board[2][1] == self.their_piece():
                return (2,0)
        if board[0][1] == self.their_piece():
                return (0,2)
        if board[0][1] == self.their_piece():
                return self.available_corner(board)
        return None
    
    


        
        
        
        
        
        
        
        
        