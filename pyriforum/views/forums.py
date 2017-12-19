from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from docutils.core import publish_parts

from pyramid.security import Authenticated

from pyramid.view import view_config

from ..models import (
    User,
    Post,
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
    if 'form.submitted' in request.params:
        body = request.params['post_body']
        new_post = Post(creator=request.user, body=body, thread=thread)
        request.dbsession.add(new_post)
    return {'thread': thread}

def rest_to_html(inpt):
    return publish_parts(inpt, writer_name='html')['html_body']


def includeme(config):
    config.commit()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.filters['restructuredtext'] = rest_to_html
