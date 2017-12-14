from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    
    #One to many relationship to Subcategory
    subcategories = relationship('Subcategory', back_populates='category')


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    
    #Many to one relationship to Category
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='subcategories')
    
    #One to many relationship to Thread
    threads = relationship('Thread', back_populates='subcategory')
