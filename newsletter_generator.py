#!/usr/bin/env python3
"""Newsletter generator CLI tool."""

import argparse
import json
import random
import re
import sys
from pathlib import Path

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


TEMPLATE_PATH = Path(__file__).parent / "newsletter_template.html"
DEFAULT_IMAGES = Path(__file__).parent / "images"
DEFAULT_OUTPUT = Path(__file__).parent / "output"

PAGE_HEIGHT = 13.4
HEADER_HEIGHT = 0.9
AD_HEIGHT = 2.6
AD_GAP = 0.1
PAGE2_HEADER = 1.0
PAGE2_FOOTER = 1.5
PAGE2_GAP = 0.2


def load_template() -> str:
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)
    return TEMPLATE_PATH.read_text()


def resolve_image(image_name: str, images_dir: Path, slot: str = "") -> str:
    if not image_name:
        return ""
    if image_name.startswith("http") or image_name.startswith("/"):
        return image_name
    if "/" in image_name or image_name.startswith("images/"):
        return image_name
    if slot:
        return f"../{images_dir.name}/{slot}/{image_name}"
    return f"../{images_dir.name}/{image_name}"


def verify_and_convert_image(img_path: Path) -> None:
    if not PIL_AVAILABLE or not img_path.exists():
        return
    try:
        img = Image.open(img_path)
        if img.format == 'TIFF' or img.mode in ('RGBA', 'LA', 'P'):
            print(f"Converting {img_path.name} from {img.format}/{img.mode} to JPEG...", file=sys.stderr)
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'LA':
                img = img.convert('RGBA')
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = background
            else:
                img = img.convert('RGB')
            img.save(img_path, 'JPEG', quality=95)
    except Exception as e:
        print(f"Warning: Could not verify {img_path.name}: {e}", file=sys.stderr)


def parse_page2_filename(filename: str) -> tuple:
    title = ""
    author = ""
    imprint = ""
    
    match = re.search(r'OF(\d+)', filename, re.IGNORECASE)
    if match:
        title = f"Offtrack Vol. {match.group(1)}"
    
    parts = filename.split('_')
    if len(parts) >= 2:
        author = parts[1].replace('-', ' ').strip()
    if len(parts) >= 3:
        imprint = parts[2].replace('-', ' ').strip()
    
    return title, author, imprint


def parse_credit_from_filename(filename: str) -> str:
    allowed_prefixes = ('ad_', 'sep_', 'by_', 'creator_', 'artist_')
    name_lower = filename.lower()
    for prefix in allowed_prefixes:
        if name_lower.startswith(prefix):
            credit = filename[len(prefix):]
            credit = re.sub(r'([a-z])([A-Z])', r'\1 \2', credit)
            credit = credit.replace('-', ' ').strip()
            credit = re.sub(r'\.(jpeg|jpg|png|gif|webp)$', '', credit, flags=re.IGNORECASE)
            if credit and credit[0].isupper():
                return credit
    return ""


def convert_markdown(text: str) -> str:
    if not MARKDOWN_AVAILABLE:
        return text
    md = markdown.Markdown()
    return md.convert(text)


def wrap_ads_in_sections(ads_html: str, separators: list = None) -> str:
    if not ads_html.strip():
        return ""
    sections = []
    styles = ["ad-style-1", "ad-style-2", "ad-style-3", "ad-style-4", "ad-style-5"]
    ads = [s.strip() for s in ads_html.split("<img ") if s.strip()]
    
    for i, ad in enumerate(ads):
        if ad.startswith("src="):
            img_tag = f"<div class='ad-section-inner'><img {ad}</div>"
        else:
            img_tag = f"<div class='ad-section-inner'>{ad}</div>"
        
        style = random.choice(styles)
        sections.append(f"<div class='ad-section {style}'>{img_tag}</div>")
        
        if separators and i < len(separators) - 1:
            sep_img = f"../{separators[i]}"
            sections.append(f"<div class='ad-separator'><img src='{sep_img}'></div>")
    
    return "\n".join(sections)


def generate_newsletter(
    ad_column_1: str,
    ad_column_2: str,
    main_content: str,
    separators: list = None,
    title: str = "",
    title_image: str = "",
    title_image_spot: bool = False,
    title2: str = "",
    page2_image: str = "",
    page2_border_image: str = "",
    page2_footer: str = "",
    sponsor_cta: str = "",
    ad_credits: str = "",
    page2_credits: str = "",
    sep_credits: str = "",
    images_dir: Path = DEFAULT_IMAGES,
) -> str:
    template = load_template()
    
    import re
    blocks = re.split(r'---|<hr\s*/?>', main_content)
    blocks = [b.strip() for b in blocks if b.strip()]
    content_parts = []
    sep3 = separators[2] if separators and len(separators) > 2 else []
    
    for i, block in enumerate(blocks):
        content_parts.append(f"<div class='content-block'>{block}</div>")
        if sep3 and i < len(sep3):
            content_parts.append(f"<div class='content-separator'><img src='../{sep3[i]}'></div>")
    
    content_html = "\n".join(content_parts) if content_parts else f"<div class='content-block'>{main_content}</div>"
    
    replacements = {
        "{{TITLE}}": title,
        "{{TITLE_IMAGE}}": title_image,
        "{{TITLE_IMAGE_SPOT}}": " title-image-spot" if title_image_spot else "",
        "{{TITLE2}}": title2,
        "{{AD_COLUMN_1}}": wrap_ads_in_sections(ad_column_1, separators[0] if separators else []),
        "{{AD_COLUMN_2}}": wrap_ads_in_sections(ad_column_2, separators[1] if separators else []),
        "{{MAIN_CONTENT}}": content_html,
        "{{PAGE2_IMAGE}}": page2_image,
        "{{PAGE2_BORDER_IMAGE}}": page2_border_image,
        "{{PAGE2_FOOTER}}": page2_footer,
        "{{SPONSOR_CTA}}": sponsor_cta,
        "{{AD_CREDITS}}": ad_credits,
        "{{PAGE2_CREDITS}}": page2_credits,
        "{{SEP_CREDITS}}": sep_credits,
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def get_max_ads_per_column() -> int:
    return 3


def auto_populate_ads_random(images_dir: Path, slot: str) -> tuple:
    slot_path = images_dir / slot
    if not slot_path.exists():
        return ("", "", [], [], [])
    
    images = sorted(slot_path.glob("*"))
    ad_images = [
        f"<img src='../{images_dir.name}/{slot}/{img.name}'>"
        for img in images
        if img.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    ]
    
    sep_path = images_dir / "separators"
    sep_list = []
    if sep_path.exists():
        sep_images = sorted(sep_path.glob("*"))
        sep_list = [f"{images_dir.name}/separators/{s.name}" for s in sep_images if s.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
    
    central_path = images_dir / "separators" / "central"
    central_list = []
    if central_path.exists():
        central_images = sorted(central_path.glob("*"))
        central_list = [f"{images_dir.name}/separators/central/{c.name}" for c in central_images if c.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
    
    if not ad_images:
        return ("", "", [], [], [])
    
    used = set()
    
    max_ads = get_max_ads_per_column()
    col1, col2 = [], []
    
    for img in ad_images:
        if img in used:
            continue
        if len(col1) < max_ads:
            col1.append(img)
            used.add(img)
        elif len(col2) < max_ads:
            col2.append(img)
            used.add(img)
        if len(col1) >= max_ads and len(col2) >= max_ads:
            break
    
    sep1 = sep_list.copy()
    sep2 = sep_list.copy()
    sep3 = central_list if central_list else sep_list.copy()
    random.shuffle(sep1)
    random.shuffle(sep2)
    random.shuffle(sep3)
    
    return ("\n".join(col1), "\n".join(col2), sep1, sep2, sep3)


def main():
    parser = argparse.ArgumentParser(description="Generate newsletter HTML")
    parser.add_argument("--ad-column-1", default="", help="First ad column content (HTML)")
    parser.add_argument("--ad-column-2", default="", help="Second ad column content (HTML)")
    parser.add_argument("--main-content", "-m", default="", help="Main content (HTML)")
    parser.add_argument("--title", "-t", default="", help="Page 1 title (HTML)")
    parser.add_argument("--title-image", default="", help="Page 1 title background image filename")
    parser.add_argument("--title-image-spot", action="store_true", help="Use title image as spot image (right-aligned)")
    parser.add_argument("--title2", default="", help="Page 2 title (HTML)")
    parser.add_argument("--page2-image", "-p", default="", help="Page 2 image filename or path")
    parser.add_argument("--page2-border-image", default="", help="Page 2 border image URL")
    parser.add_argument("--page2-footer", default="", help="Page 2 footer content (HTML)")
    parser.add_argument("--sponsor-cta", default="", help="Sponsor call to action text (HTML)")
    parser.add_argument("--images", default=DEFAULT_IMAGES, type=Path, help="Images folder path")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible results")
    parser.add_argument("--auto-ads", action="store_true", help="Auto-populate ads from images/ads folder")
    parser.add_argument("--markdown", action="store_true", help="Parse content as Markdown")
    parser.add_argument("--config", "-c", type=Path, help="JSON config file with all content")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT / "newsletter.html", help="Output file path")
    parser.add_argument("--pdf", action="store_true", help="Also generate PDF version")
    parser.add_argument("--print", action="store_true", help="Print output to stdout instead of writing file")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    use_markdown = args.markdown
    
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        
        main_content_path = config.get("main_content", "")
        if main_content_path and Path(main_content_path).exists():
            with open(main_content_path) as mf:
                md_content = mf.read()
            if MARKDOWN_AVAILABLE:
                md = markdown.Markdown()
                config["main_content"] = md.convert(md_content)
            else:
                config["main_content"] = md_content
        
        ad_column_1 = config.get("ad_column_1", "")
        ad_column_2 = config.get("ad_column_2", "")
        main_content = config.get("main_content", "")
        title = config.get("title", "")
        title_image = config.get("title_image", "")
        title_image_spot = config.get("title_image_spot", False)
        title2 = config.get("title2", "")
        page2_image = config.get("page2_image", "")
        page2_border_image = config.get("page2_border_image", "")
        page2_footer = config.get("page2_footer", "")
        sponsor_cta = config.get("sponsor_cta", "")
        images_dir = Path(config.get("images_dir", args.images))
        auto_ads = config.get("auto_ads", False)
        use_markdown = config.get("markdown", False) or args.markdown
        generate_pdf = config.get("pdf", False) or args.pdf
    else:
        ad_column_1 = args.ad_column_1
        ad_column_2 = args.ad_column_2
        main_content = args.main_content
        title = args.title
        title_image = args.title_image
        title_image_spot = args.title_image_spot
        title2 = args.title2
        page2_image = args.page2_image
        page2_border_image = args.page2_border_image
        page2_footer = args.page2_footer
        sponsor_cta = args.sponsor_cta
        images_dir = args.images
        auto_ads = args.auto_ads
        use_markdown = args.markdown
        generate_pdf = args.pdf

    separators = []
    if auto_ads:
        ad_column_1, ad_column_2, sep1, sep2, sep3 = auto_populate_ads_random(images_dir, "ads")
        separators = [sep1, sep2, sep3]

    page2_img = resolve_image(page2_image, images_dir, "page2") if page2_image else ""
    title_img = resolve_image(title_image, images_dir, "title") if title_image else ""
    
    page2_folder = images_dir / "page2"
    page2_credits = ""
    if not page2_image and page2_folder.exists():
        page2_files = [f for f in page2_folder.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
        if page2_files:
            selected = random.choice(page2_files)
            verify_and_convert_image(selected)
            page2_img = resolve_image(selected.name, images_dir, "page2")
            title_from_file, author_from_file, imprint_from_file = parse_page2_filename(selected.stem)
            if title_from_file:
                title2 = f"<h2>{title_from_file}</h2>"
            
            credit_parts = []
            if author_from_file:
                credit_parts.append(f"By {author_from_file}")
            if imprint_from_file:
                credit_parts.append(f"Published by {imprint_from_file}")
            page2_credits = " | ".join(credit_parts) if credit_parts else ""
    
    credits_path = images_dir / "credits.json"
    ad_credits_html = ""
    if auto_ads:
        ad_folder = images_dir / "ads"
        if ad_folder.exists():
            ad_files = [f for f in ad_folder.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
            credit_lines = []
            
            has_credits_json = credits_path.exists()
            credits_data = {}
            if has_credits_json:
                with open(credits_path) as f:
                    credits_data = json.load(f)
            
            for img_path in ad_files:
                verify_and_convert_image(img_path)
                credit_text = None
                if img_path.name in credits_data:
                    credit_text = credits_data[img_path.name]
                else:
                    parsed_credit = parse_credit_from_filename(img_path.name)
                    if parsed_credit:
                        credit_text = f"By {parsed_credit}"
                    elif PIL_AVAILABLE:
                        try:
                            img = Image.open(img_path)
                            if hasattr(img, '_getexif') and img._getexif():
                                exif = img._getexif()
                                if exif:
                                    comment = exif.get(0x9286) or exif.get(0x0132)
                                    if comment:
                                        credit_text = comment.decode('utf-8', errors='ignore').strip()
                        except:
                            pass
                
                if credit_text:
                    credit_lines.append(f"<span class='ad-credits-inline'>{credit_text}</span>")
            
            if credit_lines:
                ad_credits_html = "".join(credit_lines)
    
    sep_credits_html = ""
    if auto_ads:
        sep_folder = images_dir / "separators"
        if sep_folder.exists():
            sep_files = [f for f in sep_folder.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
            sep_credit_lines = []
            for img_path in sep_files:
                verify_and_convert_image(img_path)
                parsed_credit = parse_credit_from_filename(img_path.name)
                if parsed_credit:
                    sep_credit_lines.append(f"<span class='ad-credits-inline'>By {parsed_credit}</span>")
            
            if sep_credit_lines:
                sep_credits_html = " | ".join(sep_credit_lines)
        
        central_folder = images_dir / "separators" / "central"
        if central_folder.exists():
            central_files = [f for f in central_folder.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]]
            for img_path in central_files:
                verify_and_convert_image(img_path)
                parsed_credit = parse_credit_from_filename(img_path.name)
                if parsed_credit:
                    sep_credits_html += f" | <span class='ad-credits-inline'>By {parsed_credit}</span>"

    if use_markdown:
        title = convert_markdown(title)
        main_content = convert_markdown(main_content)
        title2 = convert_markdown(title2)
        page2_footer = convert_markdown(page2_footer)
        sponsor_cta = convert_markdown(sponsor_cta)

    html = generate_newsletter(
        ad_column_1, ad_column_2, main_content, separators, title, title_img,
        title_image_spot, title2, page2_img, page2_border_image, page2_footer, sponsor_cta, ad_credits_html, page2_credits, sep_credits_html, images_dir
    )

    if args.print:
        print(html)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html)
        print(f"Newsletter generated: {args.output}")
        
        if generate_pdf:
            if not PLAYWRIGHT_AVAILABLE:
                print("Error: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
            else:
                pdf_path = args.output.with_suffix(".pdf")
                html_path = args.output.absolute()
                with sync_playwright() as pw:
                    browser = pw.chromium.launch()
                    page = browser.new_page()
                    page.goto(f"file://{html_path}")
                    page.pdf(
                        path=str(pdf_path),
                        print_background=True,
                        display_header_footer=False,
                        margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                        height="14in",
                        width="8.5in"
                    )
                    browser.close()
                print(f"PDF generated: {pdf_path}")


if __name__ == "__main__":
    main()
