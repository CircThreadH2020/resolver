import argparse

from DOM_resolver import __version__


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Replace this text with your description"
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    return parser.parse_args()


def main():
    import uvicorn
    from api import app
    uvicorn.run(app, host="0.0.0.0", port=20005)


if __name__ == "__main__":
    main()
