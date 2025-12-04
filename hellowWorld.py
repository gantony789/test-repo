import sys

#!/usr/bin/env python3
"""hellowWorld.py - simple Hello World script."""


def main(name: str = "world") -> None:
    print(f"Hello, {name}!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(" ".join(sys.argv[1:]))
    else:
        main()