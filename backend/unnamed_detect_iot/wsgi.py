"""
WSGI config for unnamed_detect_iot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .REFERENCE import project_name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

application = get_wsgi_application()
