from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

Base = declarative_base()


class Line(Base):
  __tablename__ = 'line'
  id = Column(Integer, primary_key=True)
  project_id = Column(Integer)
  longitude = Column(Float)
  latitude = Column(Float)


class Category(Base):
  __tablename__ = 'category'
  id = Column(Integer, primary_key=True)
  cat = Column(Integer)
  line_id = Column(Integer)


class LineSchema(SQLAlchemyAutoSchema):

  class Meta:
    model = Line
    include_relationships = True
    include_fk = True


class CategorySchema(SQLAlchemyAutoSchema):

  class Meta:
    model = Category
    include_relationships = True
    include_fk = True
