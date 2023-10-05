from project import *
import os
from unittest.mock import patch


def test_db_name():
    current_directory = os.getcwd()
    file_to_check = FILE_PATH  
    file_path = os.path.join(current_directory, file_to_check)    
    assert os.path.exists(file_path) == True

def test_db():
    assert SELECT_TABLE() != {}

def test_question_Box_positive():
    with patch('builtins.input', side_effect=['y']):
        result = question_Box("Are you sure? (yes/no)")
    assert result == 1

def test_question_Box_negative():
    with patch('builtins.input', side_effect=['n']):
        result = question_Box("Are you sure? (yes/no)")
    assert result == 2


def test_confirm_save_db():
    with patch('builtins.input', side_effect=['n','y']):
        result = confirm_save_db("Are you sure? (yes/no)", pd=None, FILE_PATH=None, db=None, log=None, db_sheet=None, log_sheet=None)
    assert result == False
