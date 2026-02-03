"""Configuration for the event tracker."""

import os

import yaml

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
_config_file = None

_DEFAULT_CITIES = [
    {"city": "Paris", "country": "France"},
    {"city": "Bangalore", "country": "India"},
    {"city": "Pune", "country": "India"},
    {"city": "Tel Aviv", "country": "Israel"},
    {"city": "Raleigh", "country": "USA"},
    {"city": "Brno", "country": "Czech Republic"},
]


def load_cities(config_file=None):
    """Load cities from YAML config file."""
    path = config_file or _config_file or DEFAULT_CONFIG_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            return data.get("cities", _DEFAULT_CITIES)
    return _DEFAULT_CITIES


def set_config_file(path):
    """Set the config file path for subsequent load_cities() calls."""
    global _config_file
    _config_file = path


def get_target_cities():
    """Get target cities, reloading from config if needed."""
    return load_cities()


TARGET_CITIES = load_cities()

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
