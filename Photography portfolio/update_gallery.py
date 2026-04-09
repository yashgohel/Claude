import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS update
css_from = '''    /* 3D Card Tilt Gallery */
    .gallery-3d-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
      margin-bottom: 1.5rem;
    }

    .gallery-3d-row.two-col {
      grid-template-columns: 2fr 1fr;
    }

    .gallery-3d-row.one-col {
      grid-template-columns: 1fr;
    }'''

css_to = '''    /* Masonry Gallery */
    .gallery-masonry {
      column-count: 3;
      column-gap: 2rem;
    }'''

html = html.replace(css_from, css_to)

css_from_photo_card = '''    .photo-card {
      position: relative;
      overflow: hidden;
      transform-style: preserve-3d;
      transition: transform 0.1s ease;
      background: var(--dark3);
    }'''

css_to_photo_card = '''    .photo-card {
      position: relative;
      overflow: hidden;
      transform-style: preserve-3d;
      transition: transform 0.1s ease;
      background: var(--dark3);
      break-inside: avoid;
      margin-bottom: 2rem;
      border-radius: 4px;
    }'''

html = html.replace(css_from_photo_card, css_to_photo_card)

css_from_img = '''    .photo-card img {
      width: 100%;
      height: 100%;
      object-fit: cover;'''

css_to_img = '''    .photo-card img {
      width: 100%;
      height: auto;
      object-fit: contain;'''

html = html.replace(css_from_img, css_to_img)

# Remove unused card-* classes
html = re.sub(r'    \.card-(tall|wide|portrait|square) \{\s*aspect-ratio: [^;]+;\s*\}', '', html)

# Responsive updates
html = re.sub(r'\.gallery-3d-row\s*\{\s*grid-template-columns: 1fr 1fr;\s*\}(\s*)\.gallery-3d-row\.two-col\s*\{\s*grid-template-columns: 1fr;\s*\}', '.gallery-masonry {\n        column-count: 2;\n      }', html)
html = re.sub(r'\.gallery-3d-row,\s*\.gallery-3d-row\.two-col\s*\{\s*grid-template-columns: 1fr;\s*\}', '.gallery-masonry {\n        column-count: 1;\n      }', html)


# Extract all cards correctly
card_pattern = r'(<div class="photo-card [^"]+" data-idx="\d+" onclick="openLightbox\(\d+\)">.*?</div>\s*</div>)'
cards = re.findall(card_pattern, html, re.DOTALL)

# strip card-tall, card-wide, card-portrait logic from cards
cleaned_cards = [re.sub(r' card-(tall|wide|portrait|square)', ' reveal', c) for c in cards]

new_gallery_inner = '      <div class="gallery-masonry">\\n'
for c in cleaned_cards:
  new_gallery_inner += '        ' + c.strip() + '\\n'
new_gallery_inner += '      </div>'

# find section title end to replace the rest till <!-- FILM STRIP -->
section_title_end = html.find('</div>', html.find('class="section-title reveal"')) + 6
film_strip_start = html.find('<!-- FILM STRIP -->')

# we need to be careful with the outer <div class="gallery-wrap">
outer_wrap_end = html.rfind('</div>', section_title_end, film_strip_start) - 4

prefix = html[:section_title_end]
suffix = html[outer_wrap_end:]

final_html = prefix + '\n\n' + new_gallery_inner + '\n\n    ' + suffix

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

