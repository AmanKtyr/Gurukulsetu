import os
import re

theme_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\dashboardtheme\v1.24.0\index.html"
target_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\templates\students\dashboard.html"

# Read theme file
with open(theme_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = 6584 # <div class="content">
end_idx = 7607 # right before <footer>

content_lines = lines[start_idx:end_idx]
content_html = "".join(content_lines)

# Process static assets
content_html = re.sub(r'src="(assets/[^"]+)"', r"src=\"{% static '\1' %}\"", content_html)
content_html = re.sub(r'href="(assets/[^"]+)"', r"href=\"{% static '\1' %}\"", content_html)

# Let's change "Ecommerce Dashboard" to "College Dashboard"
content_html = content_html.replace("Ecommerce Dashboard", "College Dashboard")

# Construct final template
final_template = f"""{{% extends 'base.html' %}}
{{% load static %}}

{{% block content %}}
{content_html}
{{% endblock %}}
"""

# Write to target
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(final_template)

print(f"Successfully injected theme content into {target_path}")
