# blog/posts.json — schema

`posts.json` is a flat JSON array of post objects. It is the single source of
truth for the blog: `tools-generate-blog-pages.py` reads it to generate
`blog/<slug>.html` + `blog/index.html`, and `tools-rebuild-footer.py` reads it
to populate the "Insights" column in the site-wide footer. A future
content-writing agent should be able to add a post by appending an object to
this array and re-running `tools-generate-blog-pages.py` — no Python editing
required.

## Fields

| Field              | Required | Notes |
|--------------------|----------|-------|
| `slug`             | yes      | URL slug. Post is generated at `blog/<slug>.html` (flat — not year-nested — so `tools-add-analytics.py`'s one-level-deep glob still reaches it). |
| `title`            | yes      | Post headline. Used in `<title>`, OG/Twitter tags, JSON-LD `headline`, and footer/index listings. |
| `meta_description` | yes      | Used as the meta description, OG/Twitter description, JSON-LD `description`, and the excerpt shown on the blog index. |
| `author`           | yes      | Human byline shown on the post (JSON-LD `author` is always the "Assemble Capital" organization regardless of this field, per site convention). |
| `date`             | yes      | Human-readable, e.g. `"November 28, 2025"` — matches the sibling TDG repo's convention. Parsed as `%B %d, %Y` to sort posts and to derive the ISO 8601 `datePublished`/`dateModified` for JSON-LD. |
| `category`         | no       | Short label (e.g. `"Market Commentary"`). Shown as an eyebrow on the post and index card if present. |
| `tags`             | no       | Array of strings. Not currently rendered anywhere; reserved for future filtering. |
| `hero_image`       | yes      | Local path under `assets/img/blog/<slug>/`, relative to the site root (e.g. `"assets/img/blog/my-post/hero.jpg"`). Used as the post's hero image and as the OG/Twitter/JSON-LD image (resolved to an absolute `https://assemble.capital/...` URL). |
| `body_html`        | yes      | Raw HTML string for the post body. Inserted as-is into the post template — write real HTML (`<p>`, `<h2>`, etc.), not Markdown. |
| `status`           | yes      | `"draft"` or `"published"`. Only `"published"` posts get a generated page, appear on the blog index, and appear in the footer's latest-posts list. Drafts are skipped entirely (no output, not a 404 stub). |
| `source_keyword`   | no       | Traceability only (e.g. the SEO keyword or content brief this post was written from). Never rendered on the site. |
| `_migration_source`| no       | Traceability only — the original Squarespace URL this post was recovered from (e.g. `"https://assemblecapital.squarespace.com/assemble-capital-blogs/<old-slug>"`), present on posts recovered from the old blog. `null` for posts authored directly in this repo. Never rendered on the site, but this is the field the `/assemble-capital-blogs/:slug` → `/blog/:slug.html` redirect in `vercel.json` relies on for confidence that old slugs match new slugs 1:1 — don't remove it from a post without checking that redirect still makes sense. |

## Example

```json
[
  {
    "slug": "example-post",
    "title": "An Example Post Title",
    "meta_description": "One or two sentences describing the post for search and social.",
    "author": "Assemble Capital",
    "date": "November 28, 2025",
    "category": "Market Commentary",
    "tags": ["los-angeles", "multifamily"],
    "hero_image": "assets/img/blog/example-post/hero.jpg",
    "body_html": "<p>Post content goes here.</p>",
    "status": "draft",
    "source_keyword": "los angeles multifamily development"
  }
]
```

## Regenerating the site after editing this file

```
python3 tools-generate-blog-pages.py   # writes blog/<slug>.html + blog/index.html
python3 tools-rebuild-footer.py        # refreshes the footer's latest-posts list sitewide
python3 tools-generate-sitemap.py      # adds new post URLs to sitemap.xml
```
