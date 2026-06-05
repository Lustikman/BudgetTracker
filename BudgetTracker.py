from argparse import ArgumentParser, Namespace

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()

parser.add_argument("a", type=int, help="the base value")
parser.add_argument("b", type=int, help="the exponent")
group.add_argument("-v", "--verbose", action="count",
                     help="try -vv")
group.add_argument("-s", "--silence", action="store_true",
                     help="generate a silent version of the output")


args : Namespace = parser.parse_args()
result: int = args.a ** args.b

match args.verbose:
    case 1:
        print("fuck you")

    case 2:
        print(f"big result {result}")

    case _:
        print(result)


