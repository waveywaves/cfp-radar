"""Static HTML generator for events."""

import os
from datetime import date

from jinja2 import Environment, FileSystemLoader

from .config import TARGET_CITIES, TOPICS


def generate_html(events: list, output_file: str) -> None:
    """Generate static HTML file from events.

    Args:
        events: List of Event objects
        output_file: Path to write HTML file to
    """
    # Sort by CFP deadline (upcoming first), then by start date
    def sort_key(e):
        cfp_priority = e.cfp_deadline if e.cfp_deadline else date(2099, 12, 31)
        return (cfp_priority, e.start_date)

    events = sorted(events, key=sort_key)

    # Setup Jinja2 templates
    templates_dir = os.path.join(os.path.dirname(__file__), "web", "templates")
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    template = env.get_template("index.html")

    cities = [c["city"] for c in TARGET_CITIES]

    html = template.render(
        events=events,
        cities=cities,
        topics=TOPICS[:8],
        selected_city=None,
        selected_topic=None,
        has_cfp=None,
        today=date.today(),
    )

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write the HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
