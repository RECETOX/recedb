import argparse

import dask.bag as db


def load(source):
    db.from_sequence(source)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")

    args = parser.parse_args()
    load(args.source)


if __name__ == "__main__":
    main()
