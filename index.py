import os
import sys

# Add the project directory to the sys.path so Vercel can find the Django project
project_home = os.path.join(os.path.dirname(__file__), 'repobase_project')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repobase_project.settings")

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
