#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 23:00:39 2019

@author: chaninlaohaphan
"""

import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as msgbox
from player import Player, MachinePlayer


class GameBoard(tk.Frame):
    
    def __init__(self, master, player1, player2):
        super().__init__(master)
        self.pack()
        
        self.p1 = player1
        self.p2 = player2
        self.p1.set_game_piece('O', 'lightblue')
        self.p2.set_game_piece('X', 'orange')
        
        self.init_board()
    
    # Initialize the frames and board positions
    def init_board(self):
        self.p1Frame = tk.Frame(self)
        self.p1Frame.pack(side=tk.LEFT, fill='y')
        
        tk.Label(self.p1Frame, text='Player 1').pack()
        tk.Label(self.p1Frame, text=self.p1.name, width=15).pack()
        tk.Label(self.p1Frame, text=self.p1.piece).pack()
        
        self.p2Frame = tk.Frame(self)
        self.p2Frame.pack(side=tk.RIGHT, fill='y')
        
        tk.Label(self.p2Frame, text='Player 2').pack()
        tk.Label(self.p2Frame, text=self.p2.name, width=15).pack()
        tk.Label(self.p2Frame, text=self.p2.piece).pack()
        
        self.gameStatus = tk.Label(self)
        self.gameStatus.pack(side=tk.BOTTOM)
        
        self.boardFrame = tk.Frame(self)
        self.boardFrame.pack()
        self.board = [[self.create_board_button(x, y) for y in range(3)]
                        for x in range(3)]
        
        self.set_turn(self.p1)
    
    def create_board_button(self, x, y):
        button = tk.Button(self.boardFrame, text=' ', 
                           font=font.Font(size=48), height=2, width=4)
        button.bind('<Button-1>', self.click_on_board)
        button.grid(row=x, column=y)
        return button
    
    def set_turn(self, player):
        self.turn = player
        
        self.gameStatus['text'] = player.name + "'s turn"
        if player is self.p1:
            self.p1Frame.config(bd=4, bg=player.color, relief='solid')
            for widget in self.p1Frame.pack_slaves():
                widget['bg'] = player.color
            self.p2Frame.config(bd=4, bg='white', relief='flat')
            for widget in self.p2Frame.pack_slaves():
                widget['bg'] = 'white'
        elif player is self.p2:
            self.p2Frame.config(bd=4, bg=player.color, relief='solid')
            for widget in self.p2Frame.pack_slaves():
                widget['bg'] = player.color
            self.p1Frame.config(bd=4, bg='white', relief='flat')
            for widget in self.p1Frame.pack_slaves():
                widget['bg'] = 'white'
        
        if self.turn.playerType == 'human':
            for buttonRow in self.board:
                for button in buttonRow:
                    button['state'] = tk.NORMAL if button['text'] == ' ' else tk.DISABLED
        elif self.turn.playerType == 'machine':
            for buttonRow in self.board:
                for button in buttonRow:
                    button['state'] = tk.DISABLED
            self.master.after(1000, self.ask_machine)
    
    def ask_machine(self):
        board = [[button['text'] for button in boardRow] for boardRow in self.board]
        x, y = self.turn.make_move(board)
#        self.gameStatus['text'] = self.turn.name + ' plays (' + str(x) + ',' + str(y) + ')'
        if (0 <= x <= 2) and (0 <= y <= 2) and self.board[x][y]['text'] == ' ':
            self.board[x][y].config(text=self.turn.piece, disabledforeground=self.turn.color)
        self.end_turn()
    
    def click_on_board(self, event):
        button = event.widget
        if button['state'] == tk.DISABLED:
            return
        button.config(text=self.turn.piece, disabledforeground=self.turn.color)
        self.end_turn()
        
    def end_turn(self):
        board = [[button['text'] for button in boardRow] for boardRow in self.board]
        result = self.check_win(board, self.turn.piece)
        if result is None:
            if all(board[x][y] != ' ' for x in range(3) for y in range(3)):
                self.game_end(None)
            elif self.turn is self.p1:
                self.set_turn(self.p2)
            elif self.turn is self.p2:
                self.set_turn(self.p1)
        else:
            self.game_end(result)
        
    def check_win(self, board, piece):
        for i in range(3):
            if all(board[i][x] == piece for x in range(3)):
                return [(i,0), (i,1), (i,2)]
            if all(board[x][i] == piece for x in range(3)):
                return [(0,i), (1,i), (2,i)]
        if all(board[i][i] == piece for i in range(3)):
            return [(0,0), (1,1), (2,2)]
        if all(board[i][2-i] == piece for i in range(3)):
            return [(0,2), (1,1), (2,0)]
        
    def game_end(self, result):
        for boardRow in self.board:
            for button in boardRow:
                button['state'] = tk.DISABLED
                
        if result is None:
            self.gameStatus['text'] = "It's a tie!!!"
        else:
            for x, y in result:
                self.board[x][y].config(disabledforeground='lightgreen')
            self.gameStatus['text'] = self.turn.name + " wins!!!"
            
        tk.Button(self, text='Rematch', command=self.rematch).pack(side=tk.BOTTOM)
        
    def rematch(self):
        for widget in self.pack_slaves():
            widget.destroy()
        self.init_board()
        
        
class PlayerSelection(tk.Frame):
    
    def __init__(self, master, title, machineClasses, playerList):
        super().__init__(master)
        self.pack()
        
        self.title = title
        self.machineClasses = machineClasses
        self.playerList = playerList
        
        self.init_window()
        
    def init_window(self):
        tk.Label(self, text='Select '+self.title).pack()
        optionFrame = tk.Frame(self)
        optionFrame.pack()
        self.inputFrame = tk.Frame(self)
        self.inputFrame.pack()
        tk.Button(self, text='Confirm', command=self.confirm_selection).pack()
        
        self.playerType = tk.StringVar()
        tk.Radiobutton(optionFrame, text='Human', variable=self.playerType, 
                       value='human', command=self.switch_player_type).pack(side=tk.LEFT)
        tk.Radiobutton(optionFrame, text='Machine', variable=self.playerType, 
                       value='machine', command=self.switch_player_type).pack(side=tk.LEFT)
        
        self.playerName = tk.Entry(self.inputFrame)
        
        botOptions = [player.__name__ for player in self.machineClasses]
        self.botSelected = tk.StringVar()
        self.botName = tk.OptionMenu(self.inputFrame, self.botSelected, *botOptions)
        
        self.playerType.set('human')
        self.switch_player_type()
        
    def switch_player_type(self):
        for widget in self.inputFrame.pack_slaves():
            widget.pack_forget()
        if self.playerType.get() == 'human':
            tk.Label(self.inputFrame, text='Name').pack(side=tk.LEFT)
            self.playerName.pack(side=tk.LEFT)
        elif self.playerType.get() == 'machine':
            tk.Label(self.inputFrame, text='Bot Name').pack(side=tk.LEFT)
            self.botName.pack(side=tk.LEFT)
    
    def confirm_selection(self):
        if self.playerType.get() == 'human':
            name = self.playerName.get()
            if name.strip() == '':
                msgbox.showerror('Error', 'You need to enter player name.')
            else:
                self.playerList.append(Player(name=name, playerType='human'))
                self.master.destroy()
        elif self.playerType.get() == 'machine':
            className = self.botSelected.get()
            if className.strip() == '':
                msgbox.showerror('Error', 'You need to select a bot.')
            else:
                print(className)
                self.playerList.append(globals()[className]())
                self.master.destroy()
            

from student1 import RandomBot, ThinkBot
from FaBot import FaBot

players = []
bots = [RandomBot, ThinkBot, FaBot]

print(MachinePlayer.__subclasses__())

root = tk.Tk()
PlayerSelection(master=root, title='Player 1', machineClasses=bots, 
                playerList=players)
root.mainloop()

# If no player returned, terminate the script
if len(players) < 1:
    raise SystemExit
    
root = tk.Tk()
PlayerSelection(master=root, title='Player 2', machineClasses=bots, 
                playerList=players)
root.mainloop()

# If no player returned, terminate the script
if len(players) < 2:
    raise SystemExit

root = tk.Tk()
GameBoard(master=root, player1=players[0], player2=players[1])
root.mainloop()
