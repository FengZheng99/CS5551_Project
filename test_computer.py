import pytest
from unittest.mock import patch, MagicMock
from GUI import ADJACENT_MAP, MILLS, MILL_TRACK, computer_move, place_random_piece, move_random_piece, fly_random_piece, remove_opponent_piece
from board import Board

@pytest.fixture
def mock_board():
    cord_mock = MagicMock()
    mill_track_mock = MagicMock()
    board = Board(cord=cord_mock, mill_track=mill_track_mock)
    board.place_piece = MagicMock()
    board.move_piece = MagicMock()
    board.remove_piece = MagicMock()
    board.is_mill = MagicMock(return_value=True)  # Assuming a mill is formed
    return board

def test_computer_move_place_phase(mock_board):
    mock_board.placed_piece = 10
    with patch('GUI.place_random_piece') as mock_place_random_piece:
        computer_move(mock_board)
        mock_place_random_piece.assert_called_once_with(mock_board)

def test_computer_move_move_phase(mock_board):
    mock_board.placed_piece = 18
    mock_board.count_piece = [0, 4]
    with patch('GUI.move_random_piece') as mock_move_random_piece:
        computer_move(mock_board)
        mock_move_random_piece.assert_called_once_with(mock_board)

@patch('GUI.random.choice')
def test_fly_random_piece(mock_random_choice, mock_board):
    # board state for flying phase (player has 3 pieces)
    mock_board.board = [1, 0, -1, 0, 1, 0, -1, 0, 1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mock_board.player = 1
    global available_adj, available_mill
    available_adj = [1, 4, 7]  # positions adjacent to player's pieces
    available_mill = [1, 4]  # positions where a mill can be formed

    # Mock the random choice to control the output
    mock_random_choice.return_value = (9, 1)  # chosen move

    fly_random_piece(mock_board)
    # Assert that board.move_piece is called
    assert mock_board.move_piece.called

@patch('GUI.random.choice')
def test_remove_opponent_piece(mock_random_choice, mock_board):
    # board state with some opponent pieces
    mock_board.board = [1, 0, -1, 0, 1, 0, -1, 0, 1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mock_board.player = 1
    global non_removeble, current_players_men
    non_removeble = [10, 11, 12]  # non-removable positions in a mill
    current_players_men = [2, 6, 9, 10, 11, 12]  # opponent pieces positions

    # Mock the random choice to control the output
    mock_random_choice.return_value = 9  # chosen piece to remove

    remove_opponent_piece(mock_board)
    # Assert that board.remove_piece is called with the right position
    mock_board.remove_piece.assert_called_with(9)

def test_place_random_piece_no_valid_positions(mock_board):
    mock_board.board = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    place_random_piece(mock_board)
    mock_board.place_piece.assert_not_called()

def test_move_random_piece_no_valid_moves(mock_board):
    mock_board.board = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
    move_random_piece(mock_board)
    mock_board.move_piece.assert_not_called()

def test_fly_random_piece_no_valid_flies(mock_board):
    mock_board.board = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
    mock_board.count_piece = [0, 3]
    fly_random_piece(mock_board)
    mock_board.move_piece.assert_not_called()

def test_computer_win_condition(mock_board, monkeypatch):
    mock_board.count_piece = [2, 5]  # Human has 2 pieces, Computer has 5
    # Mock the print function to prevent actual printing during the test
    mock_print = MagicMock()
    monkeypatch.setattr('builtins.print', mock_print)

    computer_move(mock_board)
    # Check if the winning message was printed
    mock_print.assert_called_with('111black win')


def test_remove_opponent_piece_in_mill(mock_board, monkeypatch):
    # Setup a board state where all opponent's pieces are in mills
    mock_board.board = [0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mock_board.player = 1
    # Mock the random.choice function to control the output
    mock_random_choice = MagicMock(return_value=2)  # Choosing the piece at position 2 to remove
    monkeypatch.setattr('random.choice', mock_random_choice)

    remove_opponent_piece(mock_board)
    # Check if the correct piece is removed, considering the mill condition
    mock_board.remove_piece.assert_called_with(2)

