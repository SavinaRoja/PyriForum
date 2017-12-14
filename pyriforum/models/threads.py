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


class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    created_at = Column(ArrowType, nullable=False)
    last_updated = Column(ArrowType, nullable=False)
    
    #Many to one relationship to Subcategory
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    subcategory = relationship('Subcategory', back_populates='threads')
    
    #Many to one relationship to Creator
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', back_populates='threads')
    
    #One to many relation to Post
    posts = relationship('Post', back_populates='thread')

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        now = arrow.utcnow()
        self.created_at = now
        self.last_updated = now
