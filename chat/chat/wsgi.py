"""
WSGI config for chat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# import socketio

from socketio_app.views import s

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

application = get_wsgi_application()
# django_app = get_wsgi_application()
# application = socket.WSGIApp(s, django_app)

# import eventlet
# import eventlet.wsgi

# eventlet.wsgi.server(eventlet.listen(('', 8080)), application)
