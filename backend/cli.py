"""Command line interface for interacting with ZeroSystem."""

import argparse
import logging
from typing import Optional
from zero_system import ZeroSystem


def run_interactive(system: ZeroSystem) -> None:
    """Launch an interactive chat loop."""
    print("=== Zero System CLI ===")
    system.dna.show_dna()
    try:
        while True:
            message = input("\U0001f464 المستخدم: ")
            if message.lower() in {"exit", "quit"}:
                break
            system.interact(message)
    except KeyboardInterrupt:
        pass


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        filename="zero_system.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(description="Zero System command line interface")
    parser.add_argument("--log", default="zero_system.log", help="path to log file")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("interactive", help="start interactive session")
    sub.add_parser("status", help="print system status")
    sub.add_parser("demo", help="run predefined usage examples")

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        filename=args.log,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    system = ZeroSystem()

    if args.command == "interactive":
        run_interactive(system)
    elif args.command == "status":
        print(system.system_status())
    elif args.command == "demo":
        system.demo_usage_examples()


if __name__ == "__main__":
    main()
