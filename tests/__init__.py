import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "one_big_thing.settings")
django.setup()
