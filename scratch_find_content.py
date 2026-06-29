import os

theme_path = r"d:\Work-Space\Industrial Prijects\Gurukulsetu\dashboardtheme\v1.24.0\index.html"
with open(theme_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

footer_start = -1
for i in range(6585, len(lines)):
    if '<footer' in lines[i]:
        footer_start = i
        break

if footer_start != -1:
    print(f"Found footer at line {footer_start+1}")
else:
    print("Footer not found")
