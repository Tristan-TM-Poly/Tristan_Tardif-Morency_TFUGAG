from __future__ import annotations

import argparse
import json

from .generator import AITGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an OAK-validated AIT packet.")
    parser.add_argument("goal", help="Goal to compile into an AIT")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    packet = AITGenerator().generate(args.goal)
    indent = 2 if args.pretty else None
    print(json.dumps(packet.to_dict(), ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
