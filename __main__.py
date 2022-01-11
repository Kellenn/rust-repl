import argparse
import os
import signal
import subprocess
from sys import exit
from textwrap import indent
from typing import List


def signal_handler(*_):
    print("\n")
    exit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--display-warnings",
        action="store_false",
        help="whether to enable compiler warnings (default: false)",
    )
    parser.add_argument(
        "-p",
        "--preserve-file",
        metavar="FILE",
        nargs="?",
        default=False,
        help="whether to preserve Rust code in a file after compilation (default: false)",
    )

    return parser.parse_args()


def main(args: argparse.Namespace):
    # Handle Ctrl+C and other termination signals from OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("--Rust REPL--", end=("\n" * 2))

    while True:
        # Double curly brackets make one literal.
        if args.display_warnings:
            setup = "#![allow(warnings)]\n\nfn main() {{\n{}\n}}"
        else:
            setup = "fn main() {{\n{}\n}}"

        stdin: List[str] = []

        # Keep accepting input until
        # A blank line is received.
        while (_input := input("\n>>> " if not stdin else "... ")) != "":
            if _input == "exit":
                exit(0)

            stdin.append(_input)

        parsed_stdin = "\n".join(stdin)
        # Rust is whitespace-insensitive but if
        # The user wants to preserve the code then
        # They will probably want it to look pretty.
        # There's not really any overhead to indent the code anyways.
        code = setup.format(indent(parsed_stdin, (" " * 4)))

        if args.preserve_file:
            file = args.preserve_file
        else:
            # Really no reason for this.
            file = f"{os.urandom(8).hex()}.rs"

        with open(file, "w") as fp:
            fp.write(code)

        proc = subprocess.run(f"rustc -o {file}.bin {file}", shell=True)

        if proc.returncode == 0:
            cwd = os.getcwd()
            subprocess.Popen(f"{cwd}/{file}.bin").wait()

        try:
            if args.preserve_file is False:
                os.remove(file)
                os.remove(f"{file}.bin")
            os.remove(f"{file}.pdb")
        except FileNotFoundError:
            continue


if __name__ == "__main__":
    args = parse_args()
    main(args)
