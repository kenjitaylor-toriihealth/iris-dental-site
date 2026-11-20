#!/usr/bin/env python3
"""Pre-publish checks for the Iris Dental Medical website.

Usage (from the site folder):  python3 tools/check_site.py
Exit code 0 = no errors (warnings are allowed).

Checks
  - every page has a title, description, Google Tag Manager, site.css and site.js
  - indexable pages have a canonical URL and are listed in sitemap.xml
  - header, footer and mobile bar are identical on every page
  - internal links, images and #anchors exist
  - booking links point to IntakeQ and carry a data-cta label
  - clinic facts are consistent (hours, phone, old booking system)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://iris-dental-medical.com/"
GTM_ID = "GTM-TZVKB3WL"
BOOK = "https://irisdental.intakeq.com/booking"
SKIP_DIRS = {"docs", "tools", "Claude outputs", ".git", "node_modules"}
TEMPLATES = {"posts/post-template.html", "post-template.html"}

errors, warnings = [], []


def rel(p):
    return p.relative_to(ROOT).as_posix()


def strip_comments(html):
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        parts = set(p.relative_to(ROOT).parts)
        if parts & SKIP_DIRS:
            continue
        yield p


def block(html, pattern):
    m = re.search(pattern, html, flags=re.S)
    return m.group(0) if m else None


def normalise(fragment, prefix):
    """Make header/footer comparable across folders."""
    s = fragment.replace(' aria-current="page"', "")
    if prefix:
        s = s.replace(f'href="{prefix}', 'href="').replace(f'src="{prefix}', 'src="')
    return re.sub(r"\s+", " ", s).strip()


def main():
    all_pages = list(pages())
    texts = {p: p.read_text(encoding="utf-8") for p in all_pages}
    ids = {p: set(re.findall(r'\bid="([^"]+)"', t)) for p, t in texts.items()}

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
    if not sitemap:
        errors.append("sitemap.xml is missing")

    reference = {}
    for p, raw in texts.items():
        name = rel(p)
        if name == "post-template.html":
            warnings.append("post-template.html (old copy in the site root) can be deleted")
            continue
        html = strip_comments(raw)
        noindex = 'name="robots" content="noindex"' in html
        prefix = "/" if name == "404.html" else "../" * name.count("/")

        # --- head essentials
        title = re.search(r"<title>(.*?)</title>", html, flags=re.S)
        if not title:
            errors.append(f"{name}: missing <title>")
        elif len(title.group(1)) > 70 and name not in TEMPLATES:
            warnings.append(f"{name}: title is {len(title.group(1))} characters (aim for 60 or fewer)")
        desc = re.search(r'<meta name="description" content="([^"]*)"', html)
        if not desc:
            errors.append(f"{name}: missing meta description")
        elif len(desc.group(1)) > 170 and name not in TEMPLATES:
            warnings.append(f"{name}: description is {len(desc.group(1))} characters (aim for 155 or fewer)")
        if html.count(GTM_ID) < 2:
            errors.append(f"{name}: Google Tag Manager snippet (head + noscript) missing")
        for asset in ("css/site.css", "js/site.js"):
            if asset not in html:
                errors.append(f"{name}: does not load {asset}")

        # --- canonical + sitemap
        if not noindex and name not in TEMPLATES:
            canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
            expected = SITE + ("" if name == "index.html" else name)
            if not canon:
                errors.append(f"{name}: missing canonical link")
            elif canon.group(1) != expected:
                errors.append(f"{name}: canonical is {canon.group(1)}, expected {expected}")
            if sitemap and f"<loc>{expected}</loc>" not in sitemap:
                errors.append(f"{name}: not listed in sitemap.xml")

        # --- shared blocks
        for key, pattern in (("header", r'<header class="site-header">.*?</header>'),
                             ("footer", r'<footer class="site-footer">.*?</footer>'),
                             ("mobile bar", r'<div class="mobile-cta">.*?</div>')):
            frag = block(html, pattern)
            if frag is None:
                errors.append(f"{name}: {key} not found")
                continue
            norm = normalise(frag, prefix)
            if key not in reference:
                reference[key] = (name, norm)
            elif reference[key][1] != norm:
                errors.append(f"{name}: {key} differs from {reference[key][0]} (update every page)")

        # --- links, images, anchors
        for attr, url in re.findall(r'\b(href|src)="([^"]+)"', html):
            url = url.replace("&amp;", "&")
            if url.startswith(("http://", "https://", "tel:", "mailto:", "data:")):
                if "reserve.ne.jp" in url:
                    errors.append(f"{name}: old booking link {url}")
                continue
            path, _, frag = url.partition("#")
            if path.startswith("/"):
                target = ROOT / path.lstrip("/")
                if path == "/":
                    target = ROOT / "index.html"
            elif path:
                target = (p.parent / path).resolve()
            else:
                target = p
            if path and not target.exists():
                errors.append(f"{name}: broken link {url}")
                continue
            if frag and target.suffix == ".html" and frag not in ids.get(target.resolve(), ids.get(target, set())):
                errors.append(f"{name}: missing anchor {url}")

        # --- booking links
        for m in re.finditer(r'<a\b[^>]*href="(https://irisdental\.intakeq\.com[^"]*)"[^>]*>', html):
            if "data-cta=" not in m.group(0):
                warnings.append(f"{name}: booking link without data-cta label")
            if not m.group(1).startswith(BOOK):
                warnings.append(f"{name}: unusual booking URL {m.group(1)}")

        # --- facts
        if re.search(r"9:30|18:00", html):
            errors.append(f"{name}: old opening hours (9:30 / 18:00) found")
        for num in re.findall(r"tel:([+\d]+)", html):
            if num != "+81462445818":
                errors.append(f"{name}: unexpected phone link tel:{num}")

    for p in [ROOT / "robots.txt", ROOT / "images" / "og-image.jpg", ROOT / "images" / "favicon.png", ROOT / "404.html"]:
        if not p.exists():
            errors.append(f"missing {rel(p)}")

    print(f"Checked {len(all_pages)} pages in {ROOT}")
    for w in warnings:
        print("  warning:", w)
    for e in errors:
        print("  ERROR:  ", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
