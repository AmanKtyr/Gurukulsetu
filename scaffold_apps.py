import os

APPS = ['students', 'teachers', 'academics', 'finance', 'transport', 'hostel', 'library', 'communication']

def scaffold():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update gurukulsetu/urls.py
    urls_path = os.path.join(base_dir, 'gurukulsetu', 'urls.py')
    with open(urls_path, 'r', encoding='utf-8') as f:
        urls_content = f.read()
        
    if 'from django.urls import path, include' not in urls_content:
        urls_content = urls_content.replace('from django.urls import path', 'from django.urls import path, include')
        
    # Append app urls to urlpatterns if not already there
    for app in APPS:
        include_str = f"    path('{app}/', include('apps.{app}.urls')),\n"
        if include_str not in urls_content:
            # find last bracket
            urls_content = urls_content.replace(']\n', f'{include_str}]\n')
            
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)
        
    for app in APPS:
        # Create urls.py
        app_urls_path = os.path.join(base_dir, 'apps', app, 'urls.py')
        with open(app_urls_path, 'w', encoding='utf-8') as f:
            f.write(f"""from django.urls import path\nfrom . import views\n\napp_name = '{app}'\n\nurlpatterns = [\n    path('', views.dashboard, name='dashboard'),\n]\n""")
            
        # Update views.py
        app_views_path = os.path.join(base_dir, 'apps', app, 'views.py')
        with open(app_views_path, 'w', encoding='utf-8') as f:
            f.write(f"""from django.shortcuts import render\n\ndef dashboard(request):\n    return render(request, '{app}/dashboard.html')\n""")
            
        # Create template
        template_dir = os.path.join(base_dir, 'templates', app)
        os.makedirs(template_dir, exist_ok=True)
        template_path = os.path.join(template_dir, 'dashboard.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(f"""{{% extends 'base.html' %}}\n\n{{% block content %}}\n  <div class="container-fluid pt-4">\n    <h1>{app.title()} Dashboard</h1>\n    <p>Welcome to the {app.title()} management module.</p>\n  </div>\n{{% endblock %}}\n""")
            
    print("Scaffolding complete!")

if __name__ == '__main__':
    scaffold()
