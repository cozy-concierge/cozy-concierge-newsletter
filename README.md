# Newsletter Generator

Generate printable newsletters with auto-populated ad images and PDF export.

## Quick Start

```bash
cd ~/opencode/newsletter
python3 newsletter_generator.py -c newsletter_config.json --pdf
```

## Commands

### Generate HTML only
```bash
python3 newsletter_generator.py -c newsletter_config.json
```
Outputs to `output/newsletter.html`

### Generate HTML + PDF
```bash
python3 newsletter_generator.py -c newsletter_config.json --pdf
```
Outputs to `output/newsletter.html` and `output/newsletter.pdf`

### Preview in terminal
```bash
python3 newsletter_generator.py -c newsletter_config.json --print
```
Prints HTML to stdout instead of writing file

### CLI flags (no config file)
```bash
python3 newsletter_generator.py -t "Title" -m "<p>Content</p>" --auto-ads --pdf
```

## Configuration

Edit `newsletter_config.json` to customize content:

```json
{
  "title": "<h2>Header Text</h2>",
  "main_content": "<p>Your main content here</p>",
  "title2": "<h2>Page 2 Header</h2>",
  "page2_image": "your-image.jpg",
  "page2_footer": "<p>Contact info</p>",
  "auto_ads": true,
  "images_dir": "./images"
}
```

### Config Fields

| Field | Description |
|-------|-------------|
| `title` | Page 1 header content (HTML or Markdown) |
| `title_image` | Page 1 title image filename (auto-populates from `images/title/` if empty) |
| `title_image_spot` | Set to `true` for spot image mode (right-aligned) |
| `main_content` | Page 1 center column content (HTML or Markdown file). Use `---` to separate sections. |
| `page1_cta` | Page 1 footer CTA text (HTML or Markdown) |
| `title2` | Page 2 header content (HTML or Markdown) |
| `page2_image` | Page 2 main image filename (auto-populates from `images/page2/` if empty) |
| `page2_border_image` | Set to `has-image-border` to enable custom border image |
| `page2_footer` | Page 2 footer content (HTML or Markdown) |
| `auto_ads` | Auto-populate ads from `images/ads/` folder |
| `images_dir` | Path to images folder |
| `markdown` | Set to `true` to parse text fields as Markdown |

### Using Markdown

Instead of writing HTML, you can use Markdown for easier formatting:

```json
{
  "title": "# Cafe Stoplight\n\n*A newsletter by Cozy Concierge*",
  "main_content": "newsletter_content.md",
  "title2": "## Featured Comic\n\nBy Cafe Stoplight",
  "sponsor_cta": "**Support us!**\n\nDonate at example.com",
  "markdown": true,
  "auto_ads": true
}
```

Or reference an external markdown file for main content:

```json
{
  "main_content": "my-article.md"
}
```

#### Markdown Syntax Examples

```markdown
# Heading 1
## Heading 2

Paragraph text with **bold** and *italic*

- Bullet point
- Another point

[Link text](https://example.com)

---

Creates a new section (horizontal line)
```

#### Key Points

- Use `---` on its own line to create new content sections
- Separate sections get automatic separators in the central column
- Run with `--markdown` flag or set `"markdown": true` in config

## Image Folders

```
newsletter/images/
├── ads/           → Ad images (auto-populated, no repeat)
├── title/         → Title header images (auto-populated)
├── separators/    → Side column separator images
│   └── central/  → Central column separators
└── page2/         → Page 2 comic images (auto-populated)
```

### Adding Ads
Drop images into `images/ads/`. Filename prefix `ad_` enables auto-credit:
- `ad_JohnDoe_PublisherName.jpeg` → "By John Doe | For Publisher Name"
- `ad_JaneSmith.jpeg` → "By Jane Smith"

### Title Image
Drop images into `images/title/`. Set `title_image_spot: true` for right-aligned spot mode.

### Page 2 Image
Drop images into `images/page2/`. Filename patterns:
- `OF1_AuthorName_PublisherName.jpeg` → "By Author Name | Published by Publisher Name"
- `OF` prefix generates title "Offtrack Vol. #"

### Separators
Drop images into `images/separators/` or `images/separators/central/`. Filename prefix `sep_` enables auto-credit:
- Main separators (`/images/separators/`): `sep_ImageDescription.jpeg` → "Image Description" (no "By")
- Central separators (`/images/separators/central/`): `sep_JaneDoe_PublisherName.jpeg` → "By Jane Doe | For Publisher Name"

## Page Structure (US Legal: 8.5" x 14")

**Page 1:**
- Header (0.9in height)
- Two ad columns (2.25in each) + main content column
- Footer with CTA + credits

**Page 2:**
- Header (1in height) with auto-generated credits
- Full-width image area
- Footer (1.5in height, 10px bottom padding for printing)

## Filename Credit Convention

| Prefix | Example | Output |
|--------|---------|--------|
| `ad_` | `ad_JohnDoe.jpeg` | "By John Doe" |
| `sep_` | `sep_JohnDoe.jpeg` | "By John Doe" |
| `OF#_` | `OF1_Author_Publisher.jpeg` | "By Author | Published by Publisher" |

Note: Credits only appear if filename has uppercase letters after the prefix (camelCase becomes spaced words).

## Dependencies

- Python 3
- Playwright (for PDF generation)
  ```bash
  pip3 install playwright
  python3 -m playwright install chromium
  ```

## Troubleshooting

### PDF has no content
Check that images are in correct folders and paths are relative from `output/` folder.

### Content overflows page
Reduce ad image count in `images/ads/` or adjust heights in template CSS.

### Fonts not loading
Internet required for Google Fonts (Inter). Falls back to system sans-serif.
