from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.security import Authenticated

from pyramid.view import view_config

from ..models import (
    User,
    Category,
    Subcategory,
    Thread,
)

@view_config(route_name='forums', renderer='../templates/forums.jinja2')
def forums(request):
    categories =request.dbsession.query(Category).all()
    return {'categories': categories}

@view_config(route_name='view_subcategory', renderer='../templates/subcategories.jinja2')
def view_subcategory(request):
    subcat = request.context.subcat
    return {'threads': subcat.threads}

@view_config(route_name='view_thread', renderer='../templates/threads.jinja2')
def view_thread(request):
    thread = request.context.thread
    return {'thread': thread}
