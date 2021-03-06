from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy_utils import ArrowType
from sqlalchemy.orm import relationship

import bcrypt
import arrow

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    pw_hash = Column(Text)
    created_at = Column(ArrowType, nullable=False)
    
    #One to many relationship to Post
    posts = relationship('Post', back_populates='creator')
    
    #One to many relationship to Thread
    threads = relationship('Thread', back_populates='creator')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.created_at = arrow.utcnow()

    def set_password(self, pw):
        hashed_pw = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.pw_hash = hashed_pw.decode('utf8')

    def check_password(self, pw):
        if self.pw_hash is not None:
            expected_hash = self.pw_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    def set_created_time(self):
       self.created_at = arrow.utcnow()

