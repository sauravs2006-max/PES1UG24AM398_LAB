POINTS = {'0': 0, '15': 1, '30': 2, '40': 3}


def _to_count(token):
    """Convert a token to a non-negative int, or None if it is not plain ASCII digits."""
    token = token.strip()
    if not token or not token.isascii() or not token.isdigit():
        return None
    return int(token)


def parse_score(text):
    """Parse 'A-B' points won. Returns (a, b) or None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('-')
    if len(parts) != 2:
        return None
    a, b = _to_count(parts[0]), _to_count(parts[1])
    if a is None or b is None:
        return None
    return a, b


def game_lead(text):
    """Lead of first player in a game score like '40-30'. Returns int or None."""
    if not isinstance(text, str):
        return None
    parts = text.split('-')
    if len(parts) != 2:
        return None
    first, second = parts[0].strip(), parts[1].strip()
    if first not in POINTS or second not in POINTS:
        return None
    return POINTS[first] - POINTS[second]


def set_spread(games_csv):
    """Max minus min of games won per set, e.g. '6,4,7' -> 3. Returns int or None."""
    if not isinstance(games_csv, str):
        return None
    games = [_to_count(g) for g in games_csv.split(',')]
    if any(g is None for g in games):
        return None
    return max(games) - min(games)


def main():
    print("==== Running parse_score ====")
    user_input = input("Enter points won as A-B (e.g. 3-2): ")
    result = parse_score(user_input)
    print("Points A and B:", result if result is not None else "invalid input")

    print("\n==== Running game_lead ====")
    user_input = input("Enter a game score (e.g. 40-30): ")
    result = game_lead(user_input)
    print("Lead in Points:", result if result is not None else "invalid input")

    print("\n==== Running set_spread ====")
    user_input = input("Enter games won per set as CSV (e.g. 6,4,7): ")
    result = set_spread(user_input)
    print("Spread:", result if result is not None else "invalid input")


if __name__ == "__main__":
    main()
