# Newsletter Image Guide

## Document Specs
- **Page size**: 8.5in × 14in (US Legal)
- **Margins**: 0.3in all sides
- **Font**: Sora (Google Fonts)

---

## Image Folder Structure

```
images/
├── ads/                    → Side column ads (randomly populated)
├── separators/
│   ├── *.jpg/png          → Left/right column separators
│   └── central/           → Central column separators
├── page2/                 → Page 2 comic images (randomly selected)
├── title/                 → Page 1 title background
└── credits.json           → Ad credits mapping
```

---

## Image Dimensions for Vendors

### Page 1 Title Background
| Property | Value |
|----------|-------|
| Width | 5.2in |
| Height | 0.9in |
| Recommended | 780 × 180 px @ 150 DPI |
| Format | PNG (transparent OK) or JPEG |

### Ad Sections (Left & Right Columns)
| Property | Value |
|----------|-------|
| Width | 2.25in per column |
| Height | 2.6in |
| Recommended | 337 × 390 px @ 150 DPI |
| Format | JPEG or PNG |

### Ad Separators (Between Ads)
| Property | Value |
|----------|-------|
| Width | 2.25in |
| Height | 0.75in max |
| Recommended | 337 × 112 px @ 150 DPI |
| Tip | Horizontal designs work best |

### Central Column Separators (Between Text Blocks)
| Property | Value |
|----------|-------|
| Width | ~3.2in |
| Height | 0.4in - 2in (variable) |
| Tip | Vertical art OK here |

### Page 2 Comic Image
| Property | Value |
|----------|-------|
| Width | 7.9in (full width minus margins) |
| Height | ~10in |
| Recommended | 1185 × 1500 px @ 150 DPI |
| Aspect ratio | A4 (8.27 × 11.69 in) |
| Tip | Design as single page comic |

---

## File Naming Conventions

### Page 2 Images → Auto-Generate Title
Use `OF` prefix to auto-generate titles:

| Filename | Generates Title |
|----------|-----------------|
| `OF1-1.jpeg` | "Offtrack Vol. 1" |
| `OF3-2.jpeg` | "Offtrack Vol. 3" |
| `OF42_comic.jpeg` | "Offtrack Vol. 42" |

- Pattern: `OF` followed by a number
- Works with: `-1`, `-2` suffixes, or anywhere in filename
- Case insensitive: `of1` = `OF1`

### Credits Mapping
Add credits in `credits.json`:
```json
{
  "image_filename.jpg": "Artist: Jane Doe",
  "IMG_1234.jpeg": "Zine: Cool Stuff"
}
```

---

## How It Works

1. **Auto-population**: Run with `"auto_ads": true` in config
2. **Random selection**: Ads and separators shuffle each run
3. **Page 2**: Randomly picks from `images/page2/`, title from filename
4. **No duplicates**: Images won't repeat on same page

---

## Tips for Vendors

1. **Export as proper JPEG** - Not just renamed TIFFs
2. **300 DPI minimum** for crisp printing
3. **CMYK** not required but supported
4. **Bleed**: Add 0.125in if you want bleed edge
5. **Test**: Run generator and check PDF before submitting
