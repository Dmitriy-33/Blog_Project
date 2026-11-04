import os

from django.core.asgi import get_asgi_application
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings.dev")

application = get_asgi_application()
