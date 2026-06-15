"""Command-line entrypoint for local COVIDash ETL runs."""

from __future__ import annotations

import argparse

from covidashflow.flows import dpc_flow, full_flow, vaccines_flow


def main() -> None:
    parser = argparse.ArgumentParser(description="Run COVIDash Prefect ETL flows.")
    parser.add_argument("flow", choices=["all", "dpc", "vaccines"], nargs="?", default="all")
    parser.add_argument("--mode", choices=["full", "delta"], default="full", help="Use full for initial loads or delta for checkpointed appends.")
    parser.add_argument("--run-id", help="Optional idempotency key recorded in etl_run_log.")
    args = parser.parse_args()

    if args.flow == "dpc":
        dpc_flow(mode=args.mode, run_id=args.run_id)
    elif args.flow == "vaccines":
        vaccines_flow(mode=args.mode, run_id=args.run_id)
    else:
        full_flow(mode=args.mode, run_id=args.run_id)


if __name__ == "__main__":
    main()
