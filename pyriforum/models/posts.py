from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ArrowType

import arrow

from .meta import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_posts')
    thread_id = Column(ForeignKey('threads.id'), nullable=False)
    thread = relationship('Thread', backref='thread_posts')
    created_at = Column(ArrowType, nullable=False)
    body = Column(Text, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.created_at = arrow.utcnow()

Index('my_index', Post.thread_id, Post.created_at)
