"""Slack notification system for CFP deadlines."""

import httpx
from datetime import date
from .collector.models import EventStore, Event
from .config import EVENTS_FILE, SLACK_WEBHOOK_URL


async def check_upcoming_cfps(days: int = 14) -> list[Event]:
    """Check for CFPs closing within the specified number of days and send notifications."""
    store = EventStore(EVENTS_FILE)
    events = store.load()

    today = date.today()
    upcoming = []

    for event in events:
        if not event.cfp_deadline:
            continue
        days_left = (event.cfp_deadline - today).days
        if 0 <= days_left <= days:
            upcoming.append(event)

    # Sort by deadline
    upcoming.sort(key=lambda e: e.cfp_deadline)

    if not upcoming:
        print("No CFPs closing soon.")
        return []

    print(f"Found {len(upcoming)} CFPs closing within {days} days")

    if SLACK_WEBHOOK_URL:
        await send_slack_notifications(upcoming)
    else:
        print("SLACK_WEBHOOK_URL not set, skipping Slack notifications")
        print("\nUpcoming CFPs:")
        for event in upcoming:
            days_left = (event.cfp_deadline - today).days
            print(f"  - {event.name} ({event.city}): {days_left} days left")

    return upcoming


async def send_slack_notifications(events: list[Event]) -> None:
    """Send Slack notifications for upcoming CFP deadlines."""
    today = date.today()

    async with httpx.AsyncClient(timeout=30.0) as client:
        for event in events:
            days_left = (event.cfp_deadline - today).days

            # Build message
            urgency = ""
            if days_left <= 3:
                urgency = ":rotating_light: URGENT: "
            elif days_left <= 7:
                urgency = ":warning: "

            cfp_link = f"<{event.cfp_url}|Submit your talk>" if event.cfp_url else f"<{event.website}|Event website>"

            message = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{urgency}*CFP closing soon: {event.name}*",
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Location:*\n{event.city}, {event.country}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event Date:*\n{event.start_date.strftime('%B %d, %Y')}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*CFP Deadline:*\n{event.cfp_deadline.strftime('%B %d, %Y')}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Days Left:*\n{days_left} day{'s' if days_left != 1 else ''}",
                            },
                        ],
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": cfp_link,
                        },
                    },
                    {"type": "divider"},
                ]
            }

            try:
                response = await client.post(SLACK_WEBHOOK_URL, json=message)
                if response.status_code == 200:
                    print(f"  Sent notification for {event.name}")
                else:
                    print(f"  Failed to notify for {event.name}: {response.status_code}")
            except Exception as e:
                print(f"  Error sending notification for {event.name}: {e}")


async def send_daily_digest(events: list[Event]) -> None:
    """Send a daily digest of all upcoming CFPs to Slack."""
    if not SLACK_WEBHOOK_URL or not events:
        return

    today = date.today()

    # Group by urgency
    urgent = []  # <= 3 days
    soon = []    # <= 7 days
    upcoming = []  # <= 14 days

    for event in events:
        if not event.cfp_deadline:
            continue
        days_left = (event.cfp_deadline - today).days
        if days_left < 0:
            continue
        elif days_left <= 3:
            urgent.append((event, days_left))
        elif days_left <= 7:
            soon.append((event, days_left))
        elif days_left <= 14:
            upcoming.append((event, days_left))

    # Build digest message
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Daily CFP Digest",
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*{today.strftime('%A, %B %d, %Y')}*",
                }
            ],
        },
    ]

    def format_events(event_list: list, header: str, emoji: str) -> None:
        if not event_list:
            return
        text = f"{emoji} *{header}*\n"
        for event, days in event_list:
            text += f"• {event.name} ({event.city}) - {days}d left\n"
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

    format_events(urgent, "Closing in 3 days or less!", ":rotating_light:")
    format_events(soon, "Closing this week", ":warning:")
    format_events(upcoming, "Closing in 2 weeks", ":calendar:")

    if len(blocks) == 2:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "No CFPs closing in the next 2 weeks."},
        })

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(SLACK_WEBHOOK_URL, json={"blocks": blocks})
            if response.status_code == 200:
                print("Daily digest sent to Slack")
            else:
                print(f"Failed to send digest: {response.status_code}")
        except Exception as e:
            print(f"Error sending digest: {e}")
