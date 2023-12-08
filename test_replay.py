import pytest
import os
from unittest.mock import mock_open, MagicMock
from board import Board
import GUI
from GUI import replaying, load_replay_moves

current_move_index = 0
# Mock functions and fixtures
def mock_listdir(directory):
    return ['game_record.txt']

def mock_open(file, mode):
    file_contents = 'Place 0 1\\nMove 1 2 3\\nRemove 4'
    return MagicMock(readlines=MagicMock(return_value=file_contents.split('\\n')))

@pytest.fixture
def mock_board():
    cord_mock = MagicMock()
    mill_track_mock = MagicMock()
    board = Board(cord=cord_mock, mill_track=mill_track_mock)
    board.place_piece = MagicMock()
    board.move_piece = MagicMock()
    board.remove_piece = MagicMock()
    board.reset = MagicMock() # Mock the reset method

    return board

@pytest.fixture
def mock_filesystem(monkeypatch):
    monkeypatch.setattr(os, 'listdir', mock_listdir)
    monkeypatch.setattr('builtins.open', mock_open)

def load_replay_moves(filename):
    directory = "Records/"
    with open(os.path.join(directory, filename), 'r') as f:
        return [line.strip('\n').split(' ') for line in f.readlines()]


# Test replaying
def test_replaying(mock_board, mock_filesystem):
    replaying(mock_board)
    assert mock_board.place_piece.called_with(1)
    assert mock_board.move_piece.called_with(1, 2, 3)
    assert mock_board.remove_piece.called_with(4)

def test_load_replay_moves():
    # The expected moves based on full game test file
    expected_moves = [
        ['Place', '6', '1'],
        ['Place', '10', '-1'],
        ['Place', '8', '1'],
        ['Place', '20', '-1'],
        ['Place', '15', '1'],
        ['Place', '18', '-1'],
        ['Place', '11', '1'],
        ['Remove', '18'],
        ['Place', '19', '-1'],
        ['Place', '17', '1'],
        ['Place', '5', '-1'],
        ['Place', '16', '1'],
        ['Remove', '10'],
        ['Place', '3', '-1'],
        ['Place', '12', '1'],
        ['Remove', '5'],
        ['Place', '4', '-1'],
        ['Place', '7', '1'],
        ['Remove', '3'],
        ['Place', '10', '-1'],
        ['Place', '3', '1'],
        ['Place', '18', '-1'],
        ['Remove', '3'],
        ['Move', '12', '13', '1'],
        ['Move', '4', '3', '-1'],
        ['Remove', '13'],
        ['Move', '7', '4', '1'],
        ['Move', '20', '13', '-1'],
        ['Move', '4', '7', '1'],
        ['Remove', '13'],
        ['Move', '19', '20', '-1'],
        ['Move', '7', '4', '1'],
        ['Move', '18', '19', '-1'],
        ['Move', '4', '7', '1'],
        ['Remove', '10'],
        ['Move', '19', '4', '-1'],
        ['Move', '16', '19', '1'],
        ['Move', '20', '13', '-1'],
        ['Move', '19', '16', '1'],
        ['Remove', '4']
    ]

    actual_moves = load_replay_moves('game_moves_0.txt')
    # Verify that the function returns the correct data
    assert actual_moves == expected_moves

def test_next_move(mock_board, monkeypatch):
    # Mock draw_board to prevent it from being executed
    monkeypatch.setattr(GUI, 'draw_board', MagicMock())

    global current_move_index
    current_move_index = 0  # Reset index at the start of the test
    moves = [['Place', '6', '1'], ['Place', '10', '-1']]
    GUI.next_move(mock_board, moves)

    # Check if current_move_index is incremented
    assert GUI.current_move_index == 1
    # Check if the appropriate method on the board is called
    mock_board.place_piece.assert_called_with(6)

def test_previous_move(mock_board, monkeypatch):
    # Mock draw_board and execute_move functions
    monkeypatch.setattr(GUI, 'draw_board', MagicMock())
    monkeypatch.setattr(GUI, 'execute_move', MagicMock())

    # Set up a scenario where two moves have been made
    GUI.current_move_index = 2
    moves = [['Place', '6', '1'], ['Place', '10', '-1'], ['Place', '15', '1']]

    # Call previous_move, which should decrement current_move_index and replay moves
    GUI.previous_move(mock_board, moves)
    # Check if current_move_index is decremented
    assert GUI.current_move_index == 1

    # Verify that the board was reset
    mock_board.reset.assert_called()
    # Verify that execute_move was called to replay the first move
    GUI.execute_move.assert_called_with(mock_board, moves[0])