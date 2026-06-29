import os
import re

theme_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\dashboardtheme\v1.24.0\index.html"
target_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\templates\partials\topbar.html"

with open(theme_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = 1488
end_idx = 1830

content_lines = lines[start_idx:end_idx]
content_html = "".join(content_lines)

# Remove display:none
content_html = content_html.replace('style="display:none;"', '')

# Process static assets
content_html = re.sub(r'src="(assets/[^"]+)"', r"src=\"{% static '\1' %}\"", content_html)
content_html = re.sub(r'href="(assets/[^"]+)"', r"href=\"{% static '\1' %}\"", content_html)

final_template = f"{{% load static %}}\n{content_html}"

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(final_template)

print(f"Successfully injected theme topbar into {target_path}")
