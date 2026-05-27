# Installation

## In Claude Cowork

If this plugin has been added to a marketplace you've subscribed to:

1. Open Cowork
2. Settings → Plugins → install `jlc-vertrieb-mittelstand`

If you want to sideload from a local clone:

1. Clone this repository
2. In Cowork: Settings → Plugins → Add local plugin → point at the cloned directory

The skills register automatically. No restart needed.

## In Claude Code

```bash
# Add the marketplace (replace with your marketplace if different)
claude plugin marketplace add [your-marketplace]

# Install
claude plugin install jlc-vertrieb-mittelstand
```

Verify:

```bash
claude plugin list
```

You should see `jlc-vertrieb-mittelstand` with four skills.

## Configuration

The plugin needs three pieces of personalization to produce useful output. Create a `settings.local.json` in any folder Cowork has access to (or at `jlc-vertrieb-mittelstand/.claude/settings.local.json` for Claude Code):

```json
{
  "consultant": {
    "name": "Your Name",
    "brand": "Your Consultancy",
    "region": "Your City / Region",
    "brand_word": "Your tagline — e.g. 'Vertrieb neu denken'",
    "substance_anchor": "20+ years B2B sales at [reference industry OEM], [certification], [optional]",
    "calendar_link": "https://your-booking-link",
    "language": "de"
  },
  "icp": {
    "industries": ["machine building", "tooling", "metalworking", "plastics"],
    "fte_min": 30,
    "fte_max": 250,
    "regions": ["DACH", "specific sub-region if narrower"]
  },
  "volume_cap": {
    "cold_touches_per_week": 30
  }
}
```

The plugin reads these values into its skills automatically. If `settings.local.json` is absent, the skills will ask interactively the first time they fire.

## Settings precedence

1. `settings.local.json` in the active Cowork folder (highest)
2. `settings.local.json` in `~/.config/jlc-vertrieb-mittelstand/`
3. `jlc-vertrieb-mittelstand/.claude/settings.local.json` (Claude Code default)
4. Interactive prompt (lowest — only when nothing else is found)

## Troubleshooting

**Skills don't fire when expected.**
Skill triggers are matched against your conversation. If you say "build outreach" the wave skill should fire; if it doesn't, try "build wave 7" or "next outreach batch" — the wave-language is what the skill listens for.

**Drafts come back generic.**
Check that `consultant.region` and `consultant.brand_word` are set in your settings. The V2 pattern depends on both being non-empty. The skill won't refuse to run without them — it will just produce template-quality output.

**ICP gates feel too tight.**
The gates are calibrated for manufacturing SME (30-250 FTE) in DACH. If you sell into a different segment, override in `settings.local.json` under `icp` — the skills consume those values.

**The plugin asks for things that should be set in settings.**
That's a fallback when `settings.local.json` is missing or under-filled. Answer once, then save the answers into `settings.local.json` so the prompt doesn't repeat.

## Uninstall

```bash
# Claude Code
claude plugin uninstall jlc-vertrieb-mittelstand
```

Or in Cowork: Settings → Plugins → toggle off.

Your `settings.local.json` is left intact; remove it manually if you want a fully clean uninstall.
