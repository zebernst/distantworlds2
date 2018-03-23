if __name__ == "__main__":
    import django
    import os
    import sys
    from pathlib import PurePath

    sys.path.append(str(PurePath(__file__).parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distantworlds2.settings.dev')
    django.setup()

    from core.models import Commander
    Commander.scrape_roster()
