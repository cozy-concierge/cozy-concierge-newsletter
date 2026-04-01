# Image Dimensions Guide

## Document Specs
- **Page size**: 8.5in × 14in (US Legal)
- **Margins**: 0.3in all sides

## Image Areas

### Ad Sections (Side Columns)
| Property | Value |
|----------|-------|
| **Width** | 2.25in |
| **Height** | 3.2in |
| **At 72 DPI** | 162 × 230 px |
| **At 150 DPI** | 337 × 480 px |
| **At 300 DPI** | 675 × 960 px |

### Ad Separators (Side Columns)
| Property | Value |
|----------|-------|
| **Width** | 2.25in (fits column) |
| **Height** | 0.5in |
| **At 72 DPI** | 162 × 36 px |
| **At 150 DPI** | 337 × 75 px |
| **At 300 DPI** | 675 × 150 px |

### Central Column Separators
| Property | Value |
|----------|-------|
| **Width** | ~3.2in |
| **Height** | 0.4in - 2in (variable) |
| **For vertical art** | Use max height of 2in |

### Page 2 Comic Area
| Property | Value |
|----------|-------|
| **Width** | ~7.9in (full width minus margins) |
| **Height** | ~10.4in (minus header/footer) |
| **Aspect ratio** | A4-ish (8.27 × 11.69 in) |
| **At 150 DPI** | 1185 × 1560 px |

### Title Background
| Property | Value |
|----------|-------|
| **Width** | ~5.2in (spans title + left columns) |
| **Height** | 1.2in |
| **At 72 DPI** | 374 × 86 px |
| **At 150 DPI** | 780 × 180 px |

## Folder Structure

```
images/
├── ads/                    → Ad section images (2.25in × 3.2in)
├── separators/
│   ├── *.jpg/png          → Side column separators (2.25in × 0.5in)
│   └── central/           → Central column separators (3.2in × variable)
├── page2/                 → Page 2 comic images (A4 sized)
└── title/                 → Title background images (5.2in × 1.2in)
```

## Tips for Hand-Drawn Graphics

1. **Ad sections**: Draw at 300 DPI minimum for crisp printing
2. **Separators**: Keep horizontal images for side columns; vertical/horizontal OK for central
3. **Page 2**: Design at A4 proportions (8.27:11.69 ratio) for best fit
4. **Backgrounds**: Use PNG with transparency for title backgrounds
