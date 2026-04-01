# GastroKalk

All-in-One toolkit for gastronomy professionals in the DACH region (Switzerland, Germany, Austria). Connects Claude with the [GastroKalk](https://gastrokalk.com) platform for recipe costing, food cost analysis, allergen detection, ingredient search, and recipe generation.

## Prerequisites

- **GastroKalk account** — Sign up at [gastrokalk.com](https://gastrokalk.com)
- **Node.js 18+**

## Setup

After installing the plugin, set two environment variables:

| Variable | Description |
|----------|-------------|
| `GASTROKALK_API_URL` | Your GastroKalk API URL (e.g. `https://www.gastrokalk.com/api`) |
| `GASTROKALK_API_KEY` | Your personal API key (find it under Settings in your GastroKalk account) |

## Skills

| Skill | Trigger examples |
|-------|-----------------|
| **gastro-kalkulation** | "Calculate recipe", "Food cost analysis", "Cost per portion" |
| **gastro-rezepte** | "Create recipe", "Search ingredient", "What can I cook with..." |
| **gastro-allergene** | "Check allergens", "Is this gluten-free?", "Allergen declaration" |

## MCP Server Tools

| Tool | Description |
|------|-------------|
| `calculate-recipe` | Calculate food cost, cost per portion, and recommended selling price |
| `search-ingredients` | Search the ingredient database by name, price, unit, or supplier |
| `generate-recipe` | Generate complete recipes with ingredients, quantities, and instructions |
| `detect-allergens` | Detect the 14 EU main allergens in ingredient lists |

## Target audience

- Executive chefs and sous chefs
- Restaurant owners and F&B managers
- Catering companies
- Gastro consultants
- Culinary schools

## Region & compliance

- Prices in CHF (Switzerland) and EUR (Germany/Austria)
- VAT rates: CH 8.1%, DE 19%/7%, AT 20%/10%
- Allergen declaration per EU Regulation 1169/2011 and Swiss LMV
- HACCP-compliant documentation

## Author

Marcel Gaertner — [GastroKalk](https://gastrokalk.com)
