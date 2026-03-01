# API Keys Reference

All API keys used across the 9 biosciences skills in this plugin.

## Required Keys

| Key | Skills | Required? | Source |
|-----|--------|-----------|--------|
| `BIOSCIENCES_API_KEY` | All (gateway) | Yes | Project maintainer |
| `BIOGRID_API_KEY` | crispr, graph-builder, proteomics | Yes | [webservice.thebiogrid.org](https://webservice.thebiogrid.org) |
| `NCBI_API_KEY` | genomics | Optional (3→10 req/s) | [ncbi.nlm.nih.gov/account](https://www.ncbi.nlm.nih.gov/account/) |
| DrugBank API key | pharmacology | Commercial license | [drugbank.com](https://www.drugbank.com) |

## `.env.example` Template

```bash
# Biosciences MCP Gateway (required for all skills)
BIOSCIENCES_API_KEY=your-gateway-key-here

# BioGRID (required for crispr, graph-builder, proteomics skills)
BIOGRID_API_KEY=your-biogrid-key-here

# NCBI Entrez (optional — increases rate limit from 3 to 10 requests/second)
NCBI_API_KEY=your-ncbi-key-here

# DrugBank (commercial — required only for pharmacology skill DrugBank endpoints)
# DRUGBANK_API_KEY=your-drugbank-key-here
```

## Security

Never commit real API keys to version control. Use `.env` files locally and add `.env` to `.gitignore`. Only `.env.example` files with placeholder values should be checked in.
