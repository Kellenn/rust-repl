import argparse
import os
import signal
import subprocess
from textwrap import indent


def signal_handler(*_):
    print("\n")
    os._exit(0)


def parse_args():
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


def main(args):
    # Handle Ctrl+C and other termination signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("--Rust REPL--", end=("\n" * 3))

    while True:
        # Double curly brackets make one literal.
        if args.display_warnings:
            setup = "#![allow(warnings)]\n\nfn main() {{\n{}\n}}"
        else:
            setup = "fn main() {{\n{}\n}}"

        stdin = []

        # Keep accepting input until
        # A blank line is received.
        while (_input := input(">>> " if not stdin else "... ")) != "":
            stdin.append(_input)

        stdin = "\n".join(stdin)
        # Rust is whitespace-insensitive but if
        # The user wants to preserve the code then
        # They will probably want it to look pretty.
        # There's not much overhead to indent the code anyways.
        code = setup.format(indent(stdin, (" " * 4)))

        # Really no reason for this.
        if args.preserve_file:
            file = args.preserve_file
        else:
            file = f"{os.urandom(8).hex()}.rs"

        with open(file, "w") as fp:
            fp.write(code)

        proc = subprocess.run(f"rustc -o {file}.bin {file}", shell=True)

        try:
            if args.preserve_file is False:
                os.remove(file)
        except FileNotFoundError:
            pass  # ???

        if proc.returncode != 0:
            continue
        else:
            cwd = os.getcwd()
            subprocess.Popen(f"{cwd}/{file}.bin").wait()

        try:
            os.remove(f"{file}.bin")
            os.remove(f"{file}.pdb")
        except FileNotFoundError:
            continue


if __name__ == "__main__":
    args = parse_args()
    main(args)
