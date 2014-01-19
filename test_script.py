from pyd2l.match import Match, InvalidMatchError


def main():
    matches = []

    for match_id in range(500, 601):
        try:
            matches.append(Match(match_id))
        except InvalidMatchError:
            pass

if __name__ == "__main__":
    main()
