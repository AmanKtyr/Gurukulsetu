import os
from bs4 import BeautifulSoup

def extract_theme():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    theme_path = os.path.join(base_dir, 'dashboardtheme', 'v1.24.0', 'index.html')
    templates_dir = os.path.join(base_dir, 'templates')
    partials_dir = os.path.join(templates_dir, 'partials')
    
    os.makedirs(partials_dir, exist_ok=True)
    
    with open(theme_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    head = soup.find('head')
    
    sidebar = soup.find('nav', class_='navbar-vertical')
    topbar = soup.find('nav', class_='navbar-top')
    footer = soup.find('footer')
    
    body = soup.find('body')
    scripts = []
    if body:
        for script in body.find_all('script', recursive=False):
            scripts.append(str(script))
            
    if sidebar:
        with open(os.path.join(partials_dir, 'sidebar.html'), 'w', encoding='utf-8') as f:
            f.write(str(sidebar))
            
    if topbar:
        with open(os.path.join(partials_dir, 'topbar.html'), 'w', encoding='utf-8') as f:
            f.write(str(topbar))
            
    if footer:
        with open(os.path.join(partials_dir, 'footer.html'), 'w', encoding='utf-8') as f:
            f.write(str(footer))
            
    base_html = f"""{{% load static %}}
<!DOCTYPE html>
<html lang="en-US" dir="ltr" data-navigation-type="default" data-navbar-horizontal-shape="default">
{str(head)}
<body>
  <main class="main" id="top">
    {{% include 'partials/sidebar.html' %}}
    {{% include 'partials/topbar.html' %}}
    
    <div class="content">
      {{% block content %}}
      {{% endblock %}}
      
      {{% include 'partials/footer.html' %}}
    </div>
  </main>
  
  {''.join(scripts)}
</body>
</html>
"""
    base_html = base_html.replace('href="assets/', 'href="{% static \'assets/')
    base_html = base_html.replace('href="vendors/', 'href="{% static \'vendors/')
    base_html = base_html.replace('.css"', '.css\' %}"')
    base_html = base_html.replace('.png"', '.png\' %}"')
    base_html = base_html.replace('.ico"', '.ico\' %}"')
    base_html = base_html.replace('.json"', '.json\' %}"')
    
    base_html = base_html.replace('src="assets/', 'src="{% static \'assets/')
    base_html = base_html.replace('src="vendors/', 'src="{% static \'vendors/')
    base_html = base_html.replace('.js"', '.js\' %}"')
    
    with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
        f.write(base_html)
        
    print("Theme extracted successfully!")

if __name__ == '__main__':
    extract_theme()
