# Newsletter Generator

Generate printable newsletters with auto-populated ad images and PDF export.

## Quick Start

```bash
cd ~/opencode/newsletter
python3 newsletter_generator.py -c sample_config.json --pdf
```

## Commands

### Generate HTML only
```bash
python3 newsletter_generator.py -c sample_config.json
```
Outputs to `output/newsletter.html`

### Generate HTML + PDF
```bash
python3 newsletter_generator.py -c sample_config.json --pdf
```
Outputs to `output/newsletter.html` and `output/newsletter.pdf`

### Preview in terminal
```bash
python3 newsletter_generator.py -c sample_config.json --print
```
Prints HTML to stdout instead of writing file

### CLI flags (no config file)
```bash
python3 newsletter_generator.py -t "Title" -m "<p>Content</p>" --auto-ads --pdf
```

## Configuration

Edit `sample_config.json` to customize content:

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
| `title` | Page 1 header content (HTML) |
| `main_content` | Page 1 center column content (HTML) |
| `title2` | Page 2 header content (HTML) |
| `page2_image` | Page 2 main image filename |
| `page2_footer` | Page 2 footer content (HTML) |
| `auto_ads` | Auto-populate ads from `images/ads/` folder |
| `images_dir` | Path to images folder |

## Image Folders

```
newsletter/images/
├── ads/           → Ad images (auto-populated, shuffled, no repeat)
└── page2/         → Page 2 main image
```

### Adding Ads
Drop images into `images/ads/` - they'll be randomly selected and split between the two columns. Images won't repeat on the same page.

### Page 2 Image
Drop your image into `images/page2/` and reference it in config:
```json
"page2_image": "your-comic-page.jpg"
```

## Page Structure

**Page 1:**
- Header (1.2in height)
- Two ad columns (2in each) + main content column
- Ads auto-calculate how many fit before overflow

**Page 2:**
- Header (1in height)
- Full-width image area (A4-compatible)
- Footer (1.5in height)

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
