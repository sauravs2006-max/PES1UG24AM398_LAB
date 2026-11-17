from hypothesis import given, strategies as st
from tennis_scoring import parse_score, game_lead, set_spread


# ---- Fuzz tests: random text / None must never crash the functions ----

@given(st.text() | st.none())
def test_parse_score_no_crash(s):
    try:
        result = parse_score(s)
    except Exception as e:
        assert False, f"parse_score crashed on {s!r} with: {type(e).__name__}: {e}"
    # invalid input -> None, valid input -> (int, int) of non-negative points
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(x, int) and x >= 0 for x in result)
    )


@given(st.text() | st.none())
def test_game_lead_no_crash(s):
    try:
        result = game_lead(s)
    except Exception as e:
        assert False, f"game_lead crashed on {s!r} with: {type(e).__name__}: {e}"
    # invalid input -> None, valid input -> lead between -3 and 3
    assert result is None or (isinstance(result, int) and -3 <= result <= 3)


@given(st.text() | st.none())
def test_set_spread_no_crash(s):
    try:
        result = set_spread(s)
    except Exception as e:
        assert False, f"set_spread crashed on {s!r} with: {type(e).__name__}: {e}"
    # invalid input -> None, valid input -> non-negative spread
    assert result is None or (isinstance(result, int) and result >= 0)


# ---- Property tests on VALID input: the fix must not break correct behaviour ----

counts = st.integers(min_value=0, max_value=10**6)
labels = st.sampled_from(['0', '15', '30', '40'])


@given(counts, counts)
def test_parse_score_valid(a, b):
    assert parse_score(f"{a}-{b}") == (a, b)


@given(labels, labels)
def test_game_lead_valid(x, y):
    lead = game_lead(f"{x}-{y}")
    assert lead == -game_lead(f"{y}-{x}")
    assert (lead == 0) == (x == y)


@given(st.lists(st.integers(min_value=0, max_value=7), min_size=1))
def test_set_spread_valid(games):
    assert set_spread(",".join(map(str, games))) == max(games) - min(games)
