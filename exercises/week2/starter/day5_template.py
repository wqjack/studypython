import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", choices=["json", "csv"], required=True)
    return parser.parse_args()


def main():
    # TODO: 按 format 选择加载器并输出 summary
    args = parse_args()
    print(args)


if __name__ == "__main__":
    main()

