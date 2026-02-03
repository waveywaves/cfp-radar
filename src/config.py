"""Configuration for the event tracker."""

import os

TARGET_CITIES = [
    {"city": "Paris", "country": "France"},
    {"city": "Bangalore", "country": "India"},
    {"city": "Pune", "country": "India"},
    {"city": "Tel Aviv", "country": "Israel"},
    {"city": "Raleigh", "country": "USA"},
    {"city": "Brno", "country": "Czech Republic"},
]

TOPICS = [
    "ci/cd",
    "continuous integration",
    "continuous delivery",
    "devops",
    "platform engineering",
    "cloud native",
    "kubernetes",
    "containers",
    "gitops",
    "tekton",
]

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
MEETUP_API_KEY = os.environ.get("MEETUP_API_KEY", "")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
