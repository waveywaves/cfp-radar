# CFP Radar

AI-powered webpage generator to discover and track tech events (CI/CD, DevOps, Platform Engineering, Cloud Native) with CFP opportunities.

<img width="3826" height="2000" alt="image" src="https://github.com/user-attachments/assets/fee98e12-853e-4385-825f-e020f2294c9d" />

See it live on: https://openshift-pipelines.github.io/cfp-radar/

## Setup

Install uv on your Fedora or macOS via brew or via curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Install dependencies
uv sync

# Set required environment variables
export GEMINI_API_KEY="your-key"
```

Set `export SLACK_WEBHOOK_URL="your-webhook-url"` if you plan to use Slack notifications.

## Configuration

Cities to track are configured in `config.yaml` in the project root:

```yaml
cities:
  - city: Paris
    country: France
  - city: Bangalore
    country: India
  - city: Pune
    country: India
  - city: Tel Aviv
    country: Israel
  - city: Raleigh
    country: USA
  - city: Brno
    country: Czech Republic
```

You can override the default config file using the `--config` argument:

```bash
uv run cfp-radar collect --config my-cities.yaml
uv run cfp-radar list --config my-cities.yaml
```

If `config.yaml` is not found, the tool falls back to built-in defaults.

## Usage

```bash
# Collect events and generate HTML (default: data/index.html)
uv run cfp-radar collect

# Collect events to custom output file
uv run cfp-radar collect ./output/events.html

# Collect without AI-powered search (faster)
uv run cfp-radar collect --no-ai

# List collected events
uv run cfp-radar list

# List events filtered by city
uv run cfp-radar list --city Paris

# List only events with open CFP
uv run cfp-radar list --cfp

# Send Slack notifications for upcoming CFP deadlines
uv run cfp-radar notify
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
