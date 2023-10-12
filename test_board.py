import os
from unittest.mock import call, mock_open, patch

import pytest

from board import Board


# Test save_recording if the file was created
class TestSaveRecording:
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
        # Setup: Delete any existing recording files
        if os.path.exists("Records/game_moves_1.txt"):
            os.remove("Records/game_moves_1.txt")
        
        # Arrange: Create a board and simulate the game moves
        board = Board("dummy_cord", "dummy_mill_track")
        board.moves = ["move1", "move2", "move3"]

        with patch("builtins.open", mock_open()) as mock_file:
            # Act: Save the recording
            board.save_recording()
            
            # Assert: Verify methods are called
            mock_file.assert_called_once_with("Records/game_moves_1.txt", "w")
            mock_file.return_value.write.assert_has_calls([call('move1'), call('move2'), call('move3')])