# Learning Center articles

The article pages in this folder (`blog/<slug>.html`) are the source of truth.

- **To edit an existing article:** change its HTML file directly, then commit and push.
  If you change its title, date or photo, also run `python3 tools-build-blog-index.py`
  so the Learning Center index matches.
- **To add a new article:** write a draft and run `tools-new-blog-post.py` (below).

Don't run `tools-generate-blog-pages.py`. It is out of date and locked: it would rebuild
every article from the old copies in `posts.json` and undo later edits.

## Adding a new article

1. Copy `blog/drafts/_example/` to `blog/drafts/<your-slug>/`.
2. Fill in `post.json` (fields below) and write the article in `body.html`.
3. Check it without changing anything:

       python3 tools-new-blog-post.py blog/drafts/<your-slug> --dry-run

4. Publish it locally:

       python3 tools-new-blog-post.py blog/drafts/<your-slug>

5. Preview `/blog/<your-slug>.html`, then commit and push to make it live.

The tool copies the page shell (header, menu, notice, full disclaimer, footer, structured
data) from a current article, so new articles always match the live design. It changes
only these files:

- `blog/<slug>.html`, the new article
- `blog/index.html`, the Learning Center index
- `blog/posts.json`, the record of the post
- `sitemap.xml`, one new entry plus the index date
- `assets/img/social/cards/blog/<slug>.jpg`, the share card

Everything is built in a temporary copy of the site first. The tool stops without changing
anything if the slug already exists, a link or image points at a missing file, or any
other file would change. Drafts in `blog/drafts/` are not deployed.

## post.json fields

| Field         | Required | Notes |
|---------------|----------|-------|
| `slug`        | yes      | URL name: lowercase words joined by hyphens. The page is `blog/<slug>.html`. |
| `title`       | yes      | Headline shown on the page, index card and share card. HTML entities like `&rsquo;` are fine. |
| `page_title`  | no       | Browser-tab and Google title, under about 60 characters. Defaults to `title`. |
| `description` | yes      | 120 to 160 characters. Used in search results, the index card and social shares. |
| `date`        | yes      | Publish date as `YYYY-MM-DD`. |
| `topic`       | yes      | Learning Center section: `sb684`, `luxury`, `tic` or `investing`. Also sets the strategy link under Related Reading. |
| `strategy`    | no       | Set to `townhomes` to point the Related Reading strategy link at the AB 1751 townhome page instead of the topic's default. |
| `hero`        | yes      | Header photo, as a path under `assets/img/` (for example `sb684-hero.jpg` or `properties/june-iv/01.jpg`). |
| `card_bg`     | no       | Photo for the share card. Defaults to `hero`. |
| `related`     | yes      | Exactly three existing article slugs for Related Reading. |
| `faq`         | no       | List of `[question, answer]` pairs for Google's FAQ data. Repeat them in `body.html` so readers see them too. |
| `keyword`     | no       | The search phrase the article targets. Recorded only, never shown. |

`body.html` holds only the article body: paragraphs, `<h2>` sections, tables and so on.
Leave out the headline, byline, notice and disclaimer; the page shell supplies them.

## posts.json

A record of every article, used to file posts into Learning Center sections (`topic`) and
to pick share-card photos (`card_bg`) for posts added with the new tool. The article text
in it may be out of date for older posts; the HTML files are what's live.
`tools-build-blog-index.py` adds any article missing from it.

`_migration_source` on older posts records the original Squarespace URL. The
`/assemble-capital-blogs/:slug` redirects in `vercel.json` rely on those slugs matching, so
don't remove it without checking those redirects.
