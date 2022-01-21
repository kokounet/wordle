from argparse import ArgumentParser


def filterfunc(length: int, blacklist: str, whitelist: str):
    known = [(0, 'r'), (1, 'o'), (-1, 't')]
    return lambda word: (
        len(word) == length
        and all(word[i] == c for i, c in known)
        and not any(c in word for c in blacklist)
        and all(c in word for c in whitelist)
    )


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("dict")
    parser.add_argument("length", type=int)
    parser.add_argument("blacklist")
    parser.add_argument("whitelist")
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.dict) as file:
        if args.dict.endswith('.dic'):
            it = iter(file)
            next(it)
            next(it)
            words = set(line.strip().split('/')[0].lower() for line in it)
        else:
            words = set(line.strip().lower() for line in file)
    
    candidates = list(filter(
        filterfunc(int(args.length), args.blacklist, args.whitelist), 
        words
    ))
    print(candidates)


if __name__ == "__main__":
    main()