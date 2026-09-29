"""Build index.html for www.telecomcrm.com from src/page.template.html.

Usage:
    python3 src/build.py                     # writes ./index.html (deployable page)
    python3 src/build.py --fragment OUT.html # also writes a head-less fragment (for Claude artifact previews)

The template holds the page markup and CSS. This script inlines the TriarIT logo sprite
(src/logo-*.inline.txt, extracted from TriarIT_logo_master.pdf), generates the TM Forum API cards,
and wraps the result in a full <head> with meta, social and favicon tags.
"""
import argparse
import html
import pathlib

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent

TMF = [
    ("TMF620", 24, "Product Catalog Management", "category, productCatalog, productOffering, productSpecification", "v5.0.0 · list, create, get, patch, replace and delete"),
    ("TMF622", 6, "Product Ordering Management", "productOrder", "v5.0.0 · list, create, get, patch, replace and delete"),
    ("TMF629", 6, "Customer Management", "customer", "v4.0 · list, create, get, patch, replace and delete"),
    ("TMF637", 5, "Product Inventory Management", "product", "v5.0.0 · list, create, get, patch and delete"),
    ("TMF639", 5, "Resource Inventory Management", "resource", "v5.0.0 · resource inventory list, create, get, patch and delete"),
    ("TMF640", 7, "Service Activation Management", "service, monitor", "v4.0.0 · service write/read plus monitor reads"),
    ("TMF641", 8, "Service Ordering Management", "serviceOrder, cancelServiceOrder", "v4.1.0 · service order lifecycle and cancellation task actions"),
    ("TMF666", 42, "Account Management", "partyAccount, billingAccount, settlementAccount, financialAccount, billingCycleSpecification, billFormat, billPresentationMedia", "v4.0.0 · list, create, get, patch, replace and delete"),
    ("TMF684", 5, "Shipment Tracking", "trackings", "v1.0.0 · list, create, get, patch and delete"),
    ("TMF685", 4, "Resource Pool Management", "reservation", "v1.0 · resource-pool reservation list, create, get and patch"),
    ("TMF687", 17, "Stock Management", "productStock, adjustProductStock, checkProductStock, reserveProductStock, queryProductStock", "v4.0.0 · stock resource actions plus adjust, check, reserve and query tasks"),
    ("TMF700", 5, "Shipping Order Management", "shippingOrder", "v4.0.0 · list, create, get, patch and replace"),
]

HEAD_META = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="AI-native telecom CRM with CPQ, pricing and attribute rules, dynamic Order Management, TM Forum API integration, and complete MCP access.">
<meta name="theme-color" content="#232526">
<meta property="og:type" content="website">
<meta property="og:title" content="Telecom CRM | AI-native CPQ &amp; Order Management">
<meta property="og:description" content="The complete telecom CRM where AI configures and operates CPQ, pricing, rules and dynamic Order Management through a complete MCP toolset.">
<meta property="og:image" content="https://www.telecomcrm.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Telecom CRM | AI-native CPQ &amp; Order Management">
<meta name="twitter:description" content="The complete telecom CRM where AI configures and operates CPQ, pricing, rules and dynamic Order Management through a complete MCP toolset.">
<meta name="twitter:image" content="https://www.telecomcrm.com/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
'''


def read_inline(name):
    vb, body = (SRC / name).read_text().split('\n', 1)
    _, _, w, h = (float(v) for v in vb.split())
    return vb, body, w, h


def build():
    tpl = (SRC / 'page.template.html').read_text()
    mvb, mbody, mw, mh = read_inline('logo-mark.inline.txt')
    lvb, lbody, lw, lh = read_inline('logo-horizontal.inline.txt')
    sprite = (
        '<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
        f'<symbol id="tri-mark" viewBox="{mvb}">{mbody}</symbol>'
        f'<symbol id="tri-logo" viewBox="{lvb}">{lbody}</symbol>'
        '</svg>'
    )
    assert sum(t[1] for t in TMF) == 134, 'TMF action counts must add up to the 134 quoted in the copy'
    cards = '\n'.join(
        f'        <article class="api" role="listitem"><header><code>{c}</code><span class="chip">{n} actions</span></header>'
        f'<h3>{html.escape(name)}</h3><p class="ents">{html.escape(ents)}</p><p class="ver">{html.escape(ver)}</p></article>'
        for c, n, name, ents, ver in TMF
    )
    page = (tpl.replace('<!--SPRITE-->', sprite)
               .replace('<!--TMF-->', cards)
               .replace('{{MW}}', f'{mw:g}').replace('{{MH}}', f'{mh:g}')
               .replace('{{LW}}', f'{lw:g}').replace('{{LH}}', f'{lh:g}'))
    assert '{{' not in page, 'unfilled placeholder in template'
    return page, sprite


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fragment', help='also write a head-less fragment to this path')
    args = ap.parse_args()

    page, sprite = build()
    if args.fragment:
        pathlib.Path(args.fragment).write_text(page)

    head_part, body_part = page.split(sprite, 1)
    head_part = head_part.replace('<title>Telecom CRM by TriarIT</title>',
                                  '<title>Telecom CRM | AI-native CPQ &amp; Order Management</title>')
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n' + HEAD_META + head_part.strip() + '\n</head>\n<body>\n'
           + sprite + body_part + '\n</body>\n</html>\n')
    (ROOT / 'index.html').write_text(doc)
    print(f'wrote {ROOT / "index.html"} ({len(doc.encode())} bytes)')


if __name__ == '__main__':
    main()
