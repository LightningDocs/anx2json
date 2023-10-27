import argparse
from anx_parser import ANX_Parser
import os


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
        parser.error(
            "argument -e/--exclude: cannot appear unless argument -v/--verbose is also provided"
        )

    # Validate that if exclude was a file path, the file exists and is a .txt file
    if args.exclude is not None and len(args.exclude) == 1:
        provided_file_path = args.exclude[0]
        valid_file = (
            os.path.exists(provided_file_path)
            and os.path.isfile(provided_file_path)
            and provided_file_path.endswith(".txt")
        )
        if not valid_file:
            parser.error(
                f"argument -e/--exclude: can't open '{provided_file_path}': Either didn't end in .txt, or could not find file"
            )

        # If it was a valid file, convert args.exclude to a list containing each line of the file as a string
        with open(provided_file_path, "r") as excludefile:
            args.exclude = [line.strip() for line in excludefile]

    return args


def main(args: argparse.Namespace):
    test(args)


def test(args: argparse.Namespace):
    # print(args)
    anx_parser = ANX_Parser(args.input)

    test = anx_parser.find_answer("unanswered test")
    # print(anx_parser.parse_TextValue(test[0]))

    test2 = anx_parser.find_answer("DOB")
    # print(anx_parser.parse_DateValue(test2[0]))

    test3 = anx_parser.find_answer("PerDiem TF")
    # print(anx_parser.parse_TFValue(test3[0]), type(anx_parser.parse_TFValue(test3[0])))

    test4 = anx_parser.find_answer("Default Interest Rate NU")
    # print(
    #     anx_parser.parse_NumValue(test4[0]), type(anx_parser.parse_NumValue(test4[0]))
    # )

    test5 = anx_parser.find_answer("Per Diem interest Delivery MC")
    # selValue = test5[0][0]
    # print(anx_parser.parse_SelValue(selValue))

    test6 = anx_parser.find_answer("Loan Documents MC")
    # print(anx_parser.parse_MCValue(test6[0]))

    test7 = anx_parser.find_answer("Guarantor Name TE")
    print(anx_parser.parse_RptValue(test7[0]))
    test7 = anx_parser.find_answer("Guarantor Owner Signer Name TE")
    print(anx_parser.parse_RptValue(test7[0]))

    # This example uses the examples/hotdocs/hotdocs_example.anx file
    # test8 = anx_parser.find_answer("B signature underlying entity 3 attorneyinfact TF")
    # print(anx_parser.parse_RptValue(test8[0]))

    # test9 = anx_parser.get_unvisited_elements(args.exclude)
    # names = [elem.get("name") for elem in test9]
    # print(f"Success: Knackly JSON saved to {os.path.abspath(args.output.name)}")
    # print(f"unvisited elements = {names}")
    # for name in names:
    #     print(name)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
