from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    NO_PERMISSION_REQUIRED,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='../templates/login.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def login(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('home')
    message = ''
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
