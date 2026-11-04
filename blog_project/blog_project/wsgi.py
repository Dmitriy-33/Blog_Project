import os

from django.core.wsgi import get_wsgi_application
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings.dev")

application = get_wsgi_application()
