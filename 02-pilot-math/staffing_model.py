#!/usr/bin/env python3
"""8pm–6am virtual gate staffing + simple P&L.

Usage:
  python3 staffing_model.py
  python3 staffing_model.py --sites 15 --price 4800
"""

from __future__ import annotations

import argparse
import math

COVERAGE_HOURS = 10  # 8pm–6am
DEFAULT_PRICE = 4800.0
LOADED_HOURLY = 20.0


def agents_needed(
    sites: int,
    attempts_per_site: float,
    window_minutes: float,
    human_rate: float,
    handle_minutes: float,
    spare_factor: float = 1.25,
) -> int:
    """Estimate agents required to clear a peak window with spare capacity."""
    human_attempts = sites * attempts_per_site * human_rate
    agent_minutes = human_attempts * handle_minutes
    busy_agents = agent_minutes / window_minutes
    return max(1, math.ceil(busy_agents * spare_factor))


def coverage_pnl(sites: int, price: float, agents: int) -> dict:
    labor = agents * LOADED_HOURLY * COVERAGE_HOURS * 30
    opex = 4000 + sites * 150
    revenue = sites * price
    return {
        "revenue": revenue,
        "labor": labor,
        "opex": opex,
        "contribution": revenue - labor - opex,
        "margin": (revenue - labor - opex) / revenue if revenue else 0,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Virtual gate 8pm–6am staffing / P&L")
    p.add_argument("--sites", type=int, default=15)
    p.add_argument("--price", type=float, default=DEFAULT_PRICE)
    args = p.parse_args()

    print("=== Coverage: 8:00pm–6:00am (10 hrs) ===")
    print("=== Peak concurrency scenarios ===")
    scenarios = [
        ("Quiet overnight (20 sites)", 20, 0.15, 60, 0.70, 2.0),
        ("Busier overnight (40 sites)", 40, 0.25, 60, 0.70, 2.0),
        ("Late evening edge 8–9pm (15 sites)", 15, 0.8, 30, 0.50, 2.5),
        ("Reference: morning rush NOT in scope (50 sites)", 50, 1.8, 15, 0.45, 2.5),
    ]
    for name, sites, attempts, window, human, handle in scenarios:
        n = agents_needed(sites, attempts, window, human, handle)
        print(f"{name}: ~{n} agents online")

    print("\n=== 8pm–6am P&L ===")
    for sites in (5, 10, 15, 20, 50):
        need = agents_needed(sites, 0.2, 60, 0.7, 2.0, spare_factor=1.3)
        agents = max(2 if sites <= 10 else 3, need)
        price = args.price if sites == args.sites else DEFAULT_PRICE
        pnl = coverage_pnl(sites, price, agents)
        print(
            f"{sites:>3} sites | {agents} agents | "
            f"rev ${pnl['revenue']:,.0f} | contrib ${pnl['contribution']:,.0f} "
            f"({pnl['margin']*100:.0f}% margin)"
        )

    print("\n=== Custom ===")
    need = agents_needed(args.sites, 0.2, 60, 0.7, 2.0, spare_factor=1.3)
    agents = max(2 if args.sites <= 10 else 3, need)
    pnl = coverage_pnl(args.sites, args.price, agents)
    print(f"Sites={args.sites} price=${args.price:,.0f}/mo agents={agents}")
    for k, v in pnl.items():
        if k == "margin":
            print(f"  {k}: {v*100:.1f}%")
        else:
            print(f"  {k}: ${v:,.0f}")


if __name__ == "__main__":
    main()
