if __name__ == "__main__":
    import django
    import os
    import sys
    from distantworlds2.settings.base import SITE_ROOT

    sys.path.append(os.path.abspath(str(SITE_ROOT)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distantworlds2.settings.dev')
    django.setup()

    from core.models import Commander
    Commander.scrape_roster()
