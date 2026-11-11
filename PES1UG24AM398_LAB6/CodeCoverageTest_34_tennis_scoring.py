"""Lab 6 - Code (line) coverage tests for tennis_scoring.py
Goal: execute every line of the module at least once (>= 90% line coverage).
"""
import pytest
from tennis_scoring import game_score, set_winner, match_status


# ---------- game_score ----------
def test_game_start():
    assert game_score(0, 0) == "0-0"

def test_game_regular_score():
    assert game_score(2, 1) == "30-15"

def test_game_negative_points_raises():
    with pytest.raises(ValueError):
        game_score(-1, 0)

def test_game_deuce():
    assert game_score(3, 3) == "deuce"

def test_game_A_wins_after_deuce():
    assert game_score(5, 3) == "game A"

def test_game_B_wins_after_deuce():
    assert game_score(3, 5) == "game B"

def test_game_advantage_A():
    assert game_score(4, 3) == "advantage A"

def test_game_advantage_B():
    assert game_score(3, 4) == "advantage B"

def test_game_A_wins_to_love():
    assert game_score(4, 0) == "game A"

def test_game_B_wins_to_fifteen():
    assert game_score(1, 4) == "game B"


# ---------- set_winner ----------
def test_set_undecided():
    assert set_winner(3, 2) is None

def test_set_A_wins_6_4():
    assert set_winner(6, 4) == "A"

def test_set_B_wins_3_6():
    assert set_winner(3, 6) == "B"

def test_set_A_wins_tiebreak():
    assert set_winner(7, 6) == "A"

def test_set_B_wins_tiebreak():
    assert set_winner(6, 7) == "B"


# ---------- match_status ----------
def test_match_A_wins():
    assert match_status(2, 0, 3) == "A wins"

def test_match_B_wins():
    assert match_status(1, 3, 5) == "B wins"

def test_match_decider():
    assert match_status(1, 1, 3) == "decider"

def test_match_in_progress():
    assert match_status(1, 0, 3) == "in progress"
