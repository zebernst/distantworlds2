if __name__ == "__main__":
    import django
    import os
    import sys

    sys.path.append(os.path.abspath('..'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distantworlds2.settings.dev')
    django.setup()

    from core.models import Commander
    Commander.scrape_roster()
