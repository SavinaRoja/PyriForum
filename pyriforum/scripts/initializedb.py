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
    Thread,
    Post,
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

        #Create a few test users
        testy = User(name='testy', email='testy@testerson.com')
        testy.set_password('testy')
        dbsession.add(testy)

        basic = User(name='basic', email='basic@basicson.com')
        basic.set_password('basic')
        dbsession.add(basic)
        
        #Create a few categories and subcategories for the forums
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
        
        #Add a few threads to the subcategories in the forums
        version = Thread(title='New Version!', subcategory=announcements, creator=testy)
        dbsession.add(version)
        opensource = Thread(title='We are open source', subcategory=announcements, creator=testy)
        dbsession.add(opensource)
        
        ramblings = Thread(title='Should I switch to SQLite', subcategory=updates, creator=basic)
        dbsession.add(ramblings)
        
        hunter2 = Thread(title='The story of hunter2', subcategory=general_chat, creator=testy)
        hunter2.posts = [Post(creator=testy, body='hey, if you type in your pw, it will show as stars'),
                         Post(creator=testy, body='********* see!'),
                         Post(creator=basic, body='hunter2'),
                         Post(creator=basic, body='doesnt look like stars to me'),
                         Post(creator=testy, body='<basic> *******'),
                         Post(creator=testy, body='thats what I see'),
                         Post(creator=basic, body='oh, really?'),
                         Post(creator=testy, body='Absolutely'),
                         Post(creator=basic, body='you can go hunter2 my hunter2-ing hunter2'),
                         Post(creator=basic, body='haha, does that look funny to you?'),
                         Post(creator=testy, body='lol, yes. See, when YOU type hunter2, it shows to us as *******'),
                         Post(creator=basic, body='thats neat, I didnt know IRC did that'),
                         Post(creator=testy, body='yep, no matter how many times you type hunter2, it will show to us as *******'),
                         Post(creator=basic, body='awesome!'),
                         Post(creator=basic, body='wait, how do you know my pw?'),
                         Post(creator=testy, body='er, I just copy pasted YOUR ******\'s and it appears to YOU as hunter2 cause its your pw'),
                         Post(creator=basic, body='oh, ok.')]
        dbsession.add(hunter2)
        

        
        
        
        


