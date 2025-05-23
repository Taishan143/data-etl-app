import argparse
from data_etl_app import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=__version__)
    # Add other command-line options here if needed/wanted
    parser.parse_args()


if __name__ == "__main__":
    main()
