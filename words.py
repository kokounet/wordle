from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass
from itertools import zip_longest
from unicodedata import normalize, category


@dataclass
class Guess:
    length: int
    absent: set[str]
    wellplaced: defaultdict[str, list[int]]
    missplaced: defaultdict[str, list[int]]


def filterfunc(guess: Guess):
    return lambda word: (
        len(word) == guess.length
        and all(all(word[i] == c for i in ii) for c, ii in guess.wellplaced.items())
        and all(
            c in word and all(word[i] != c for i in ii)
            for c, ii in guess.missplaced.items()
        )
        and all(c not in guess.absent for c in word)
    )


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("dict")
    parser.add_argument("guesses", nargs="+")
    return parser.parse_args()


def parse_guesses(guesses: list[str]) -> Guess:
    blacklist = set()
    wellplaced = defaultdict(list)
    missplaced = defaultdict(list)
    for guess in guesses:
        length = 0
        offset = 0
        for i, (curr, next) in enumerate(zip_longest(guess, guess[1:])):
            if not curr.isalpha():
                offset += 1
                continue
            length += 1
            match next:
                case "!":
                    wellplaced[curr].append(i - offset)
                case "?":
                    missplaced[curr].append(i - offset)
                case _:
                    if curr not in missplaced or curr not in wellplaced:
                        blacklist.add(curr)
    return Guess(length, blacklist, wellplaced, missplaced)


def unaccented(word: str) -> str:
    return "".join(c for c in normalize("NFD", word) if category(c) != "Mn")


def read_dict(path: str) -> set[str]:
    with open(path, encoding="utf-8") as file:
        if path.endswith(".dic"):
            it = iter(file)
            next(it)
            next(it)
            words = set(line.strip().split("/")[0].lower() for line in it)
        else:
            words = set(line.strip().lower() for line in file)

    words = set(unaccented(word) for word in words)
    return words


def main():
    args = parse_args()
    words = read_dict(args.dict)
    guesses = parse_guesses(args.guesses)
    candidates = sorted(filter(filterfunc(guesses), words))
    print(candidates)


if __name__ == "__main__":
    main()
