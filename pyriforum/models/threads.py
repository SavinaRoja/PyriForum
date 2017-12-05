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
    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_threads')
    title = Column(String(50))
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=False)
    created_at = Column(ArrowType, nullable=False)
    last_updated = Column(ArrowType, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.created_at = arrow.utcnow()
