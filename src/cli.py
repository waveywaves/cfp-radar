"""CLI entry point for the event tracker."""

import argparse
import asyncio
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Tech Events & CFP Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Collect command
    collect_parser = subparsers.add_parser("collect", help="Collect events from all sources")
    collect_parser.add_argument(
        "output_file",
        nargs="?",
        default="data/index.html",
        help="HTML output file (default: data/index.html)",
    )
    collect_parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip AI-powered web search (faster, but fewer results)",
    )

    # Notify command
    notify_parser = subparsers.add_parser("notify", help="Send Slack notifications for upcoming CFPs")
    notify_parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Notify for CFPs closing within this many days (default: 14)",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List collected events")
    list_parser.add_argument("--city", help="Filter by city")
    list_parser.add_argument("--topic", help="Filter by topic")
    list_parser.add_argument("--cfp", action="store_true", help="Show only events with open CFP")

    args = parser.parse_args()

    if args.command == "collect":
        asyncio.run(cmd_collect(args))
    elif args.command == "notify":
        asyncio.run(cmd_notify(args))
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)


async def cmd_collect(args):
    """Run event collection."""
    from datetime import date
    from .collector.agent import collect_all_events
    from .collector.models import EventStore
    from .config import EVENTS_FILE

    print("Collecting events from all sources...")
    use_ai = not args.no_ai

    if not use_ai:
        print("(AI search disabled)")

    await collect_all_events(use_ai=use_ai)

    # Read all events from store (includes previously collected)
    store = EventStore(EVENTS_FILE)
    events = store.filter(start_after=date.today())
    print(f"\nTotal events: {len(events)}")

    # Show summary
    cfp_events = [e for e in events if e.cfp_deadline]
    print(f"  - With CFP: {len(cfp_events)}")

    upcoming_cfp = [e for e in cfp_events if e.cfp_deadline >= date.today()]
    print(f"  - Open CFP: {len(upcoming_cfp)}")

    # Generate static HTML
    from .generator import generate_html
    generate_html(events, args.output_file)
    print(f"\nHTML output written to: {args.output_file}")


async def cmd_notify(args):
    """Send Slack notifications."""
    from .notifier import check_upcoming_cfps

    print(f"Checking for CFPs closing within {args.days} days...")
    await check_upcoming_cfps(days=args.days)


def cmd_list(args):
    """List events."""
    from datetime import date
    from .collector.models import EventStore
    from .config import EVENTS_FILE

    store = EventStore(EVENTS_FILE)
    events = store.filter(
        city=args.city,
        topic=args.topic,
        has_cfp=True if args.cfp else None,
        start_after=date.today(),
    )

    if not events:
        print("No events found matching the criteria.")
        return

    # Sort by CFP deadline
    def sort_key(e):
        return e.cfp_deadline if e.cfp_deadline else date(2099, 12, 31)

    events.sort(key=sort_key)

    for event in events:
        cfp_info = ""
        if event.cfp_deadline:
            days_left = (event.cfp_deadline - date.today()).days
            cfp_info = f" [CFP: {event.cfp_deadline} ({days_left}d)]"

        print(f"{event.start_date} | {event.name} | {event.city}{cfp_info}")


if __name__ == "__main__":
    main()
