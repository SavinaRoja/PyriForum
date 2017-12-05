from pyramid.config import Configurator
from pyramid.security import Authenticated

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.set_default_permission('view')
    config.scan()
    return config.make_wsgi_app()
