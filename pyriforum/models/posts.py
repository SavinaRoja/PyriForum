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
    created_at = Column(ArrowType, nullable=False)
    body = Column(Text, nullable=False)
    
    #Many to one relationship to User
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', back_populates='posts')
    
    #Many to one relationship to Thread
    thread_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
    thread = relationship('Thread', back_populates='posts')


    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.created_at = arrow.utcnow()
