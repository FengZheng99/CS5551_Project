import os
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

from board import ADJACENT_MAP, BLACK, MILL_MAP, MILLS, WHITE, Board


class TestBoard:
    def test_creation(self):
        board = Board("dummy_cord", "dummy_mill_track")
        board.moves = ["move1", "move2", "move3"]
        board.save_recording()
        assert os.path.exists("Records/game_moves_1.txt")
    
    def test_sequence(self):
        if os.path.exists("Records/game_moves_1.txt"):
            os.remove("Records/game_moves_1.txt")
        board = Board("dummy_cord", "dummy_mill_track")
        board.moves = ["move3", "move1", "move2"]
        board.save_recording()

        with open("Records/game_moves_1.txt", "r") as f:
            contents = f.read()
        expected_contents = "move3move1move2"
        assert contents == expected_contents
        
    def test_file_closure(self):
        if os.path.exists("Records/game_moves_1.txt"):
            os.remove("Records/game_moves_1.txt")
        
        board = Board("dummy_cord", "dummy_mill_track")
        board.moves = ["move1", "move2", "move3"]

        with patch("builtins.open", mock_open()) as mock_file:
            board.save_recording()
            
            mock_file.assert_called_once_with("Records/game_moves_1.txt", "w")
            mock_file.return_value.write.assert_has_calls([call('move1'), call('move2'), call('move3')])
            
    def test_automatic_turn_switch(self):
        game = Board("dummy_cord", "dummy_mill_track")
        game.player = 1
        game.change_turn()
        assert game.player == -1
    
    # Test for game_over when player has fewer than three pieces
    def test_game_over_fewer_than_three_pieces(self, capsys):
        # Setup the board
        board = Board(MILL_MAP, MILLS)
        board.count_current_piece = [2, 4]  # Assuming index 0 is for BLACK, who has fewer than 3 pieces
        board.player = BLACK
        board.move_file = MagicMock()  # Mock the move_file attribute
        # Call the game_over method
        board.game_over()
        # Capture the output
        captured = capsys.readouterr()
        # Test if the correct message was printed to the console
        assert "Player 1 has fewer than three pieces." in captured.out

    # Test for game_over when player has no valid moves
    def test_game_over_no_valid_moves(self,capsys):
        # Setup the board
        board = Board(MILL_MAP, MILLS)
        board.count_current_piece = [3, 4]  # BLACK has 3 pieces
        board.player = BLACK
        board.move_file = MagicMock()
        board.has_no_valid_moves = MagicMock(return_value=True)  # Stubbing to simulate no valid moves
        board.game_over()
        captured = capsys.readouterr()
        assert "Player 1 has no valid moves." in captured.out
        
    # Test if move_file is closed when game_over is called
    def test_exit_game_calls_move_file_close(self):
        # Create a MagicMock
        mock_move_file = MagicMock()
        mock_move_file.closed = False
        mock_mill_map = MagicMock()
        mock_mills = MagicMock()
        # Instantiate the Board
        board = Board(mock_mill_map, mock_mills)
        # Set the move_file attribute to the mock
        board.move_file = mock_move_file
        board.count_current_piece = [2,4]
        board.player = BLACK
        # Call the method that close move_file
        board.game_over()
        # Assert that the close method was called on the mock_move_file
        mock_move_file.close.assert_called_once()