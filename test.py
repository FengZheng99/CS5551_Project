import pytest
import pygame
from board import Board
import GUI as G

CORD = [(200, 50), (400, 50), (600, 50),
        (266, 116), (400, 116), (534, 116),
        (334, 184), (400, 184), (466, 184),
        (200, 250), (266, 250), (334, 250), 
        (466, 250), (534, 250), (600, 250),
        (334, 316), (400, 316), (466, 316),
        (266, 384), (400, 384), (534, 384),
        (200, 450), (400, 450), (600, 450)
        ]

MILL_TRACK = {
        'm1': 0, 'm2': 0, 'm3': 0, 'm4': 0,
        'm5': 0, 'm6': 0, 'm7': 0, 'm8': 0,
        'm9': 0, 'm10': 0, 'm11': 0, 'm12': 0,
        'm13': 0, 'm14': 0, 'm15': 0, 'm16': 0
}

board = Board(CORD, MILL_TRACK)

def test_change_turn():
    board.player = 1
    board.change_turn()
    assert board.player == -1

def test_successful_place_piece():
    board.board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    mouse = (200, 50)
    G.place_piece_rule(board, mouse)
    assert board.board[0] == 1

def test_unsuccessful_place_piece():
    board.board = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    mouse = (200, 50)
    G.place_piece_rule(board, mouse)
    assert board.board[0] == -1

def test_successful_move_piece():
    board.board = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    global move_from
    move_from = None
    mouse = (200, 50)
    G.move_piece_rule(board, mouse)
    mouse = (400, 50)
    G.move_piece_rule(board, mouse)
    assert board.board[1] == 1

def test_unsuccessful_move_piece():
    board.board = [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    global move_from
    move_from = None
    mouse = (200, 50)
    G.move_piece_rule(board, mouse)
    mouse = (400, 50)
    G.move_piece_rule(board, mouse)
    assert board.board[1] == -1

def test_successful_fly_piece():
    board.board = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    global move_from
    move_from = None
    mouse = (200, 50)
    G.black_fly_rule(board, mouse)
    mouse = (600, 450)
    G.black_fly_rule(board, mouse)
    assert board.board[23] == 1

def test_unsuccessful_fly_piece():
    board.board = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    board.player = 1
    global move_from
    move_from = None
    mouse = (200, 50)
    G.black_fly_rule(board, mouse)
    mouse = (600, 450)
    G.black_fly_rule(board, mouse)
    assert board.board[23] == -1

def test_successful_removal_of_an_opponent_piece():
    board.board = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    board.player = 1
    board.mill_list(1)
    mouse = (600, 450)
    G.mill_rule(board, mouse)
    assert board.board[23] == 0

def test_unsuccessful_removal_of_an_opponent_piece_in_mill():
    board.board = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1]
    board.player = 1
    board.mill_list(1)
    board.mill_list(-1)
    mouse = (600, 450)
    G.mill_rule(board, mouse)
    assert board.board[23] == -1

def test_successful_removal_of_an_opponent_piece_in_mill():
    board.board = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1]
    board.player = 1
    board.mill_list(1)
    board.mill_list(-1)
    mouse = (600, 450)
    G.mill_rule(board, mouse)
    assert board.board[23] == 0

def test_no_available_moves():
    board.board = [1, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board.player = 1
    assert board.has_no_valid_moves()

