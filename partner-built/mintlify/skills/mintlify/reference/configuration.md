# Configuration reference

Full docs.json settings, snippets, hidden pages, and custom CSS/JS.

## docs.json

The `docs.json` file controls the entire site. Required fields: `theme`, `name`, `colors.primary`, and `navigation`.

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Your Docs",
  "colors": {
    "primary": "#3B82F6"
  },
  "navigation": {
    "groups": [
      {
        "group": "Getting started",
        "pages": ["index", "quickstart"]
      }
    ]
  }
}
```

## Complete frontmatter fields

The SKILL.md file lists common frontmatter fields. Here is the complete set:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Page title in navigation and browser tabs. |
| `description` | string | No | Brief description for SEO. Displays under the title. |
| `sidebarTitle` | string | No | Short title for sidebar navigation. |
| `icon` | string | No | Lucide, Font Awesome, or Tabler icon name. Also accepts a URL or file path. |
| `iconType` | string | No | Font Awesome icon style: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`. |
| `tag` | string | No | Label next to page title in sidebar (e.g., "NEW"). |
| `hidden` | boolean | No | Remove from sidebar. Page still accessible by URL. |
| `noindex` | boolean | No | Prevent search engine indexing. |
| `mode` | string | No | Page layout: `default`, `wide`, `custom`, `frame`, `center`. |
| `keywords` | array | No | Search terms for internal search and SEO. |
| `api` | string | No | API endpoint for interactive playground (e.g., `"POST /users"`). |
| `openapi` | string | No | OpenAPI endpoint reference (e.g., `"GET /endpoint"`). |
| `url` | string | No | External URL. Makes the nav entry link externally. |
| `timestamp` | boolean | No | Override global timestamp setting for this page. |

## Page modes

Control page layout with the `mode` frontmatter field.

```yaml
# Default: standard layout with sidebar and table of contents
---
title: "Page title"
---

# Wide: hides table of contents for extra horizontal space
---
title: "Page title"
mode: "wide"
---

# Custom: blank canvas, only top navbar visible
---
title: "Page title"
mode: "custom"
---

# Frame: like custom but keeps sidebar (Aspen, Almond, and Luma themes only)
---
title: "Page title"
mode: "frame"
---

# Center: removes sidebar and TOC, centers content (Mint and Linden themes only)
---
title: "Page title"
mode: "center"
---
```

## Theme

One of: `mint`, `maple`, `palm`, `willow`, `linden`, `almond`, `aspen`, `sequoia`, `luma`.

| Theme | Character |
|-------|-----------|
| `mint` | Classic, time-tested |
| `maple` | Modern, clean, good for AI/SaaS |
| `palm` | Sophisticated, fintech-focused |
| `willow` | Stripped-back, minimal |
| `linden` | Retro terminal, monospace |
| `almond` | Card-based, minimalist |
| `aspen` | Modern, supports complex navigation |
| `sequoia` | Minimal, elegant, large-scale content |

## Colors

```json
"colors": {
  "primary": "#3B82F6",
  "light": "#F8FAFC",
  "dark": "#0F172A"
}
```

- `primary` (required): Main color, generally for emphasis in light mode.
- `light`: Color for emphasis in dark mode.
- `dark`: Color for buttons and hover states.

All values must be hex codes starting with `#`.

## Logo

```json
"logo": {
  "light": "/logo/light.svg",
  "dark": "/logo/dark.svg",
  "href": "https://example.com"
}
```

## Favicon

Single file or light/dark variants:

```json
"favicon": "/favicon.ico"
```

```json
"favicon": {
  "light": "/favicon.png",
  "dark": "/favicon-dark.png"
}
```

## Icons

```json
"icons": {
  "library": "lucide"
}
```

Options: `lucide` or `fontawesome`. You can only use one library per project. Individual icons can still use URLs or file paths regardless of this setting.

## Fonts

```json
"fonts": {
  "family": "Inter"
}
```

Google Fonts load automatically by family name. For custom fonts:

```json
"fonts": {
  "family": "CustomFont",
  "source": "/fonts/CustomFont.woff2",
  "format": "woff2",
  "weight": 400,
  "heading": {
    "family": "HeadingFont",
    "weight": 700
  },
  "body": {
    "family": "BodyFont",
    "weight": 400
  }
}
```

## Appearance

```json
"appearance": {
  "default": "system",
  "strict": false
}
```

- `default`: `"system"`, `"light"`, or `"dark"`.
- `strict`: Set `true` to hide the light/dark mode toggle.

## Background

```json
"background": {
  "image": {
    "light": "/bg-light.svg",
    "dark": "/bg-dark.svg"
  },
  "decoration": "gradient",
  "color": {
    "light": "#FFFFFF",
    "dark": "#000000"
  }
}
```

- `decoration`: `"gradient"`, `"grid"`, or `"windows"`.

## Styling

```json
"styling": {
  "eyebrows": "breadcrumbs",
  "latex": true,
  "codeblocks": {
    "theme": {
      "light": "github-light",
      "dark": "github-dark"
    }
  }
}
```

- `eyebrows`: `"section"` (default) or `"breadcrumbs"`.
- `latex`: Override automatic LaTeX detection.
- `codeblocks`: `"system"` (default), `"dark"`, a Shiki theme name, or an object with `light`/`dark` themes.

## Navbar

```json
"navbar": {
  "links": [
    {
      "label": "Community",
      "href": "https://example.com/community"
    },
    {
      "type": "github",
      "href": "https://github.com/example/repo"
    }
  ],
  "primary": {
    "type": "button",
    "label": "Get Started",
    "href": "https://example.com/start"
  }
}
```

Link types: omit `type` for standard text link, `"github"` for repo with star count, `"discord"` for server with online count.

Primary button types: `"button"`, `"github"`, `"discord"`.

## Footer

```json
"footer": {
  "socials": {
    "x": "https://x.com/example",
    "github": "https://github.com/example",
    "linkedin": "https://linkedin.com/company/example"
  },
  "links": [
    {
      "header": "Resources",
      "items": [
        { "label": "Blog", "href": "https://example.com/blog" }
      ]
    }
  ]
}
```

Valid social keys: `x`, `website`, `facebook`, `youtube`, `discord`, `slack`, `github`, `linkedin`, `instagram`, `hacker-news`, `medium`, `telegram`, `bluesky`, `threads`, `reddit`, `podcast`.

## Banner

```json
"banner": {
  "content": "Version 2.0 is live! [Learn more](/changelog)",
  "dismissible": true
}
```

Supports basic Markdown in content (links, bold, italic). Language-specific banners can be set inside the `navigation.languages` entries.

## Redirects

```json
"redirects": [
  {
    "source": "/old-page",
    "destination": "/new-page",
    "permanent": true
  }
]
```

## Metadata

```json
"metadata": {
  "timestamp": true
}
```

Shows "Last modified on [date]" on all pages. Override per-page with `timestamp` frontmatter.

## Interaction

```json
"interaction": {
  "drilldown": false
}
```

Controls whether clicking a navigation group navigates to its first page (`true`) or only expands/collapses (`false`).

## SEO

```json
"seo": {
  "metatags": {
    "canonical": "https://docs.example.com",
    "og:locale": "en_US"
  },
  "indexing": "navigable"
}
```

- `indexing`: `"navigable"` (only nav pages) or `"all"` (every page including hidden).

## Search

```json
"search": {
  "prompt": "Search documentation..."
}
```

## Contextual menu

```json
"contextual": {
  "options": ["copy", "chatgpt", "claude", "cursor", "vscode"]
}
```

Options: `copy`, `view`, `chatgpt`, `claude`, `perplexity`, `mcp`, `cursor`, `vscode`, or custom objects.

## Thumbnails

```json
"thumbnails": {
  "appearance": "light",
  "background": "/images/thumbnail-bg.svg",
  "fonts": {
    "family": "Inter"
  }
}
```

## Error handling

```json
"errors": {
  "404": {
    "redirect": true,
    "title": "Page not found",
    "description": "This page doesn't exist."
  }
}
```

## API configuration

```json
"api": {
  "openapi": "openapi.json",
  "playground": {
    "display": "interactive",
    "proxy": true
  },
  "examples": {
    "languages": ["bash", "javascript", "python"],
    "defaults": "all",
    "prefill": false,
    "autogenerate": true
  },
  "mdx": {
    "server": "https://api.example.com",
    "auth": {
      "method": "bearer"
    }
  }
}
```

- `openapi`: Single file, array, or object with `source` and `directory`.
- `asyncapi`: Same format as `openapi` for AsyncAPI specs.
- `playground.display`: `"interactive"`, `"simple"`, or `"none"`.
- `examples.languages`: `bash`, `go`, `java`, `javascript`, `node`, `php`, `powershell`, `python`, `ruby`, `swift`.
- `examples.defaults`: `"required"` or `"all"` (include optional params).
- `mdx.auth.method`: `"bearer"`, `"basic"`, `"key"`, `"cobo"`.

## Integrations

```json
"integrations": {
  "ga4": { "measurementId": "G-XXXXXXXXXX" },
  "gtm": { "tagId": "GTM-XXXXX" },
  "posthog": { "apiKey": "phc_xxx", "apiHost": "https://app.posthog.com" },
  "amplitude": { "apiKey": "xxx" },
  "mixpanel": { "projectToken": "xxx" },
  "segment": { "key": "xxx" },
  "clarity": { "projectId": "xxx" },
  "fathom": { "siteId": "xxx" },
  "hotjar": { "hjid": "xxx", "hjsv": "xxx" },
  "logrocket": { "appId": "xxx" },
  "heap": { "appId": "xxx" },
  "pirsch": { "id": "xxx" },
  "plausible": { "domain": "xxx", "server": "optional" },
  "hightouch": { "writeKey": "xxx", "apiHost": "optional" },
  "clearbit": { "publicApiKey": "xxx" },
  "intercom": { "appId": "xxx" },
  "frontchat": { "snippetId": "xxx" },
  "telemetry": { "enabled": true },
  "cookies": { "key": "consent_key", "value": "accepted" }
}
```

## Reusable snippets

Store reusable content in the `/snippets/` directory.

### MDX snippets

```mdx
<!-- snippets/prerequisites.mdx -->
Before you begin, make sure you have:
- Node.js 18+
- A Mintlify account
```

Import in any page:

```mdx
import Prerequisites from "/snippets/prerequisites.mdx";

<Prerequisites />
```

### JSX components

```jsx
// snippets/counter.jsx
export const Counter = () => {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(count - 1)}>-</button>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
};
```

Import in any page:

```mdx
import { Counter } from "/snippets/counter.jsx";

<Counter />
```

JSX components must be in `/snippets/`. Nested imports between snippets are not supported.

## Hidden pages

Set `hidden: true` in frontmatter to remove from sidebar. Page remains accessible by URL.

```yaml
---
title: "Internal reference"
hidden: true
---
```

Or omit the page from `docs.json` navigation entirely.

## .mintignore

Exclude files completely from the published docs. Place `.mintignore` in the docs root. Uses `.gitignore` syntax.

```
drafts/
*.draft.mdx
private-notes.md
**/internal/**
!important.mdx
```

Files in `.mintignore` are not published, not indexed, and not accessible by URL.

## Custom CSS and JavaScript

### CSS

Add `.css` files to your repository. Class names become available in all MDX files.

```css
/* styles.css */
#navbar {
  background: #fffff2;
}
```

Built-in Tailwind CSS v3 classes are available. Arbitrary values (e.g., `w-[350px]`) are not supported — use inline `style` instead.

### JavaScript

Any `.js` file in the content directory is included globally on all pages.
