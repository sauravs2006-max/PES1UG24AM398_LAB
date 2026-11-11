"""Lab 6 - Branch coverage tests for tennis_scoring.py
Goal: make every decision (if) evaluate to BOTH True and False,
including each side of compound 'and'/'or' conditions and boundary values
(>= 90% branch coverage).
"""
import pytest
from tennis_scoring import game_score, set_winner, match_status


# =====================================================================
# game_score
# =====================================================================

# if a < 0 or b < 0  -> True via a, True via b, and False
@pytest.mark.parametrize("a, b", [(-1, 0), (0, -1), (-3, -2)])
def test_game_negative_raises(a, b):
    with pytest.raises(ValueError, match="negative points"):
        game_score(a, b)

# if a >= 3 and b >= 3  -> False path, each operand False separately
@pytest.mark.parametrize("a, b, expected", [
    (0, 0, "0-0"),
    (1, 2, "15-30"),
    (3, 2, "40-30"),     # a >= 3 True, b >= 3 False
    (2, 3, "30-40"),     # a >= 3 False (short-circuit)
    (3, 0, "40-0"),
    (0, 3, "0-40"),
])
def test_game_before_deuce_zone(a, b, expected):
    assert game_score(a, b) == expected

# Inside the deuce zone (a >= 3 and b >= 3 True) - every nested branch
def test_game_deuce_3_3():
    assert game_score(3, 3) == "deuce"

def test_game_deuce_long_rally():
    assert game_score(10, 10) == "deuce"                      # a == b True

def test_game_A_wins_by_two_in_deuce_zone():
    assert game_score(5, 3) == "game A"                       # a-b >= 2 True

def test_game_B_wins_by_two_in_deuce_zone():
    assert game_score(6, 8) == "game B"                       # b-a >= 2 True

def test_game_advantage_A():
    assert game_score(4, 3) == "advantage A"                  # a > b True

def test_game_advantage_B():
    assert game_score(7, 8) == "advantage B"                  # a > b False

# Outside the deuce zone, a >= 4 / b >= 4 both ways
def test_game_A_wins_outside_deuce_zone():
    assert game_score(4, 2) == "game A"                       # a >= 4 True

def test_game_B_wins_outside_deuce_zone():
    assert game_score(2, 4) == "game B"                       # a>=4 F, b>=4 T

def test_game_B_wins_to_love():
    assert game_score(0, 4) == "game B"


# =====================================================================
# set_winner
# =====================================================================

# if a >= 6 and a - b >= 2
def test_set_A_wins_6_0():
    assert set_winner(6, 0) == "A"

def test_set_A_wins_7_5():
    assert set_winner(7, 5) == "A"

def test_set_A_six_but_not_two_clear():
    assert set_winner(6, 5) is None        # a>=6 True, a-b>=2 False

def test_set_A_two_clear_but_below_six():
    assert set_winner(5, 3) is None        # a>=6 False (short-circuit)

# if b >= 6 and b - a >= 2
def test_set_B_wins_0_6():
    assert set_winner(0, 6) == "B"

def test_set_B_wins_5_7():
    assert set_winner(5, 7) == "B"

def test_set_B_six_but_not_two_clear():
    assert set_winner(5, 6) is None        # b>=6 True, b-a>=2 False

# Tiebreak checks: if a == 7 and b == 6 / if b == 7 and a == 6
def test_set_A_wins_tiebreak():
    assert set_winner(7, 6) == "A"

def test_set_B_wins_tiebreak():
    assert set_winner(6, 7) == "B"

def test_set_a_is_7_but_b_not_6():
    assert set_winner(7, 7) is None        # a==7 True, b==6 False; b==7 True, a==6 False

def test_set_six_all():
    assert set_winner(6, 6) is None        # a==7 False, b==7 False

def test_set_undecided():
    assert set_winner(3, 2) is None


# =====================================================================
# match_status
# =====================================================================

@pytest.mark.parametrize("sets_a, sets_b, best_of, expected", [
    (2, 0, 3, "A wins"),
    (2, 1, 3, "A wins"),
    (3, 2, 5, "A wins"),
    (0, 2, 3, "B wins"),
    (1, 3, 5, "B wins"),
    (1, 1, 3, "decider"),
    (2, 2, 5, "decider"),
    (0, 0, 3, "in progress"),
    (1, 0, 3, "in progress"),    # sets_a == needed-1 True, sets_b False
    (0, 1, 3, "in progress"),    # sets_a == needed-1 False (short-circuit)
    (2, 1, 5, "in progress"),
    (0, 0, 1, "decider"),        # best of 1: the only set decides
    (1, 0, 1, "A wins"),
])
def test_match_status(sets_a, sets_b, best_of, expected):
    assert match_status(sets_a, sets_b, best_of) == expected
