import argparse
import json
import os
from pprint import pprint

from anx_parser import ANX_Parser
from knackly_writer import Knackly_Writer


def parse_arguments() -> argparse.Namespace:
    """Return the args Namespace after validating that args have been provided correctly"""

    def init_argparse() -> argparse.ArgumentParser:
        """Create the ArgumentParser object"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i",
            "--input",
            required=True,
            type=argparse.FileType("r", encoding="UTF-8"),
            help="input file path",
        )
        parser.add_argument(
            "-o",
            "--output",
            required=True,
            type=argparse.FileType("w"),
            help="output file path",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="print information about the conversion",
        )
        parser.add_argument(
            "-e",
            "--exclude",
            nargs="+",
            help="""specify which .anx answers should be excluded from verbose message (requires verbose). 
            This should be either:
                - a path to a .txt file, where each line in the file is the name of an Answer element to be excluded, 
                - multiple strings, where each string is the name of an Answer element""",
        )
        return parser

    parser = init_argparse()
    args = parser.parse_args()

    # Validate that if exclude was provided, verbose must have also been provided
    if args.exclude is not None and args.verbose is False:
        parser.error("argument -e/--exclude: cannot appear unless argument -v/--verbose is also provided")

    # Validate that if exclude was a file path, the file exists and is a .txt file
    if args.exclude is not None and len(args.exclude) == 1:
        provided_file_path = args.exclude[0]
        valid_file = os.path.exists(provided_file_path) and os.path.isfile(provided_file_path) and provided_file_path.endswith(".txt")
        if not valid_file:
            parser.error(f"argument -e/--exclude: can't open '{provided_file_path}': Either didn't end in .txt, or could not find file")

        # If it was a valid file, convert args.exclude to a list containing each line of the file as a string
        with open(provided_file_path, "r") as excludefile:
            args.exclude = [line.strip() for line in excludefile]

    return args


def main(args: argparse.Namespace):
    writer = Knackly_Writer(ANX_Parser(args.input))
    args.input.close()
    writer.create()

    json.dump(writer.json, args.output, indent=2)
    print(f"Success! Saved output to {os.path.abspath(args.output.name)}")
    args.output.close()

    if args.verbose:
        print("\n--- UNUSED ELEMENTS ---")

        unvisited_elements = writer.anx.get_unvisited_elements(args.exclude)
        for idx, e in enumerate(unvisited_elements, start=1):
            print(idx, e.get("name"))


def test(args: argparse.Namespace):
    print(args)
    anx_parser = ANX_Parser(args.input)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
    # test(args)
