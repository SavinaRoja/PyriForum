from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.security import Authenticated

from pyramid.view import view_config

from ..models import User, Category, Subcategory

@view_config(route_name='home', renderer='../templates/homepage.jinja2')
def home(request):
    return dict()

@view_config(route_name='forums', renderer='../templates/forums.jinja2')
def forums(request):
    categories =request.dbsession.query(Category).all()
    return {'categories': categories}
        
