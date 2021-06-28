"""
ASGI config for unnamed_detect_iot_ project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from .REFERENCE import project_name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

application = get_asgi_application()
