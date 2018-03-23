if __name__ == "__main__":
    import django
    import os
    import sys
    import inspect
    from pathlib import PurePath

    root = PurePath(os.path.abspath(inspect.getfile(inspect.currentframe()))).parent.parent
    sys.path.append(str(root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distantworlds2.settings.dev')
    django.setup()

    from core.models import Commander
    Commander.scrape_roster()
