# Tech Events & CFP Tracker

AI-powered tool to discover and track tech events (CI/CD, DevOps, Platform Engineering, Cloud Native) with CFP opportunities.

## Target Cities

- Paris, France
- Bangalore, India
- Pune, India
- Tel Aviv, Israel
- Raleigh, USA
- Brno, Czech Republic

## Setup

install uv on your fedora or macos via brew or via curl

```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Install dependencies
uv sync

# Set required environment variables
export GEMINI_API_KEY="your-key"
```

Set `export SLACK_WEBHOOK_URL="your-webhook-url"` if you plan to slack notifications

## Usage

```bash
# Collect events and generate HTML (default: data/index.html)
uv run gather-cnf collect

# Collect events to custom output file
uv run gather-cnf collect ./output/events.html

# Collect without AI-powered search (faster)
uv run gather-cnf collect --no-ai

# Send Slack notifications for upcoming CFP deadlines
uv run gather-cnf notify
```

## Output

The `collect` command generates a static HTML file at `data/index.html` by default. Open this file in a browser to view events.

## Copyright

[Apache-2.0](./LICENSE)

## Authors

### Chmouel Boudjnah

- Fediverse - <[@chmouel@chmouel.com](https://fosstodon.org/@chmouel)>
- Twitter - <[@chmouel](https://twitter.com/chmouel)>
- Blog  - <[https://blog.chmouel.com](https://blog.chmouel.com)>
