#!/usr/bin/env python3
import sys
from dotenv import load_dotenv

load_dotenv()

from foundry_run import run_single_turn  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/run_agent.py "<prompt>"")
        raise SystemExit(2)

    prompt = sys.argv[1]
    out = run_single_turn(prompt)
    print(out)


if __name__ == "__main__":
    main()
