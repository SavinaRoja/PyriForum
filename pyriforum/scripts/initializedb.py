import bcrypt
import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import (
    Category,
    Subcategory,
    User,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        user = User(name='testy', email='testy@testerson.com')
        user.set_password('testy')
        dbsession.add(user)

        basic = User(name='basic', email='basic@basicson.com')
        basic.set_password('basic')
        dbsession.add(basic)
        
        general = Category(name='General')
        announcements = Subcategory(name='Announcements',
                                    description='General news and happenings')
        updates = Subcategory(name='DevLog',
                              description='Updates and ramblings of the dev team')
        general.subcategories = [announcements, updates]
        dbsession.add(general)
        
        suggestions = Category(name='Suggestions')
        site_suggestions = Subcategory(name='Site Suggestions',
                                       description='Have an idea for the site? Let\'s discuss!')
        feedback = Subcategory(name='Feedback',
                               description='Tell us how we are doing')
        suggestions.subcategories = [site_suggestions, feedback]
        dbsession.add(feedback)
        
        discussion = Category(name='Site Discussion')
        general_chat = Subcategory(name='General Chat',
                                   description='Discuss anything about the site')
        originals = Subcategory(name='Original Work',
                                description='Share what you\'ve done or are working on')
        intros = Subcategory(name='Introductions',
                             description='New to the site? Say hello!')
        discussion.subcategories = [general_chat, originals, intros]
        dbsession.add(discussion)
        
        


