import argparse
from anx_parser import ANX_Parser


def init_argparse() -> argparse.ArgumentParser:
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
    return parser


def main(args: argparse.Namespace):
    test(args)


def test(args: argparse.Namespace):
    # print(args)
    anx_parser = ANX_Parser(args.input)

    # test = anx_parser.find_answer("unanswered test")
    # print(anx_parser.parse_TextValue(test[0]))

    # test2 = anx_parser.find_answer("DOB")
    # print(anx_parser.parse_DateValue(test2[0]))

    # test3 = anx_parser.find_answer("PerDiem TF")
    # print(anx_parser.parse_TFValue(test3[0]), type(anx_parser.parse_TFValue(test3[0])))

    # test4 = anx_parser.find_answer("Default Interest Rate NU")
    # print(
    #     anx_parser.parse_NumValue(test4[0]), type(anx_parser.parse_NumValue(test4[0]))
    # )

    # test5 = anx_parser.find_answer("Per Diem interest Delivery MC")
    # selValue = test5[0][0]
    # print(anx_parser.parse_SelValue(selValue))

    # test6 = anx_parser.find_answer("Loan Documents MC")
    # print(anx_parser.parse_MCValue(test6[0]))


if __name__ == "__main__":
    args = init_argparse().parse_args()
    main(args)
