import os

APPS = ['students', 'teachers', 'academics', 'finance', 'transport', 'hostel', 'library', 'communication']

def update_sidebar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sidebar_path = os.path.join(base_dir, 'templates', 'partials', 'sidebar.html')
    
    html = """<nav class="navbar navbar-vertical navbar-expand-lg">
  <div class="collapse navbar-collapse" id="navbarVerticalCollapse">
    <div class="navbar-vertical-content">
      <ul class="navbar-nav flex-column" id="navbarVerticalNav">
        <li class="nav-item">
          <p class="navbar-vertical-label">School Management</p>
          <hr class="navbar-vertical-line"/>
        </li>
"""
    for app in APPS:
        html += f"""
        <li class="nav-item">
          <div class="nav-item-wrapper">
            <a class="nav-link label-1" href="{{% url '{app}:dashboard' %}}" role="button">
              <div class="d-flex align-items-center">
                <span class="nav-link-icon"><span data-feather="grid"></span></span>
                <span class="nav-link-text-wrapper"><span class="nav-link-text">{app.title()}</span></span>
              </div>
            </a>
          </div>
        </li>
"""
    html += """
      </ul>
    </div>
  </div>
</nav>
"""
    with open(sidebar_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Sidebar updated!")

if __name__ == '__main__':
    update_sidebar()
