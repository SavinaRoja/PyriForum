from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', factory=authenticated_factory)
    config.add_route('login', '/login', factory=authenticated_factory)
    config.add_route('logout', '/logout', factory=authenticated_factory)
    #config.add_route('view_page', '/{pagename}', factory=page_factory)
    #config.add_route('add_page', '/add_page/{pagename}',
                     #factory=new_page_factory)
    #config.add_route('edit_page', '/{pagename}/edit_page',
                     #factory=page_factory)

def authenticated_factory(request):
    return AuthenticatedACL()

class AuthenticatedACL(object):
    #An ACL rule tuple is (Allow/Deny, PrincipleString, PermissionString)
    __acl__ = [(Allow, Authenticated, 'view'),
              ]

#def new_page_factory(request):
    #pagename = request.matchdict['pagename']
    #if request.dbsession.query(Page).filter_by(name=pagename).count() > 0:
        #next_url = request.route_url('edit_page', pagename=pagename)
        #raise HTTPFound(location=next_url)
    #return NewPage(pagename)

#class NewPage(object):
    #def __init__(self, pagename):
        #self.pagename = pagename

    #def __acl__(self):
        #return [
            #(Allow, 'role:editor', 'create'),
            #(Allow, 'role:basic', 'create'),
        #]

#def page_factory(request):
    #pagename = request.matchdict['pagename']
    #page = request.dbsession.query(Page).filter_by(name=pagename).first()
    #if page is None:
        #raise HTTPNotFound
    #return PageResource(page)

#class PageResource(object):
    #def __init__(self, page):
        #self.page = page

    #def __acl__(self):
        #return [
            #(Allow, Everyone, 'view'),
            #(Allow, 'role:editor', 'edit'),
            #(Allow, str(self.page.creator_id), 'edit'),
        #]
