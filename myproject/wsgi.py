"""
WSGI config for saveyourvote project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

# activate_this
projectdir = os.path.dirname(os.path.realpath(__file__))
activate_this = os.path.join(projectdir, '../my-env/bin/activate_this.py')
activate_this = os.path.realpath(activate_this)
execfile(activate_this, dict(__file__=activate_this))

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
projectname = os.path.basename(projectdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % projectname)

# Calculate the path based on the location of the WSGI script
sys.path.append(os.path.realpath(os.path.join(projectdir, '..')))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
