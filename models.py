from sqlalchemy import Column, Integer, String, Float
from database import Base

class Moduler(Base):
    __tablename__ = "moduler"

    id = Column(Integer, primary_key=True, index=True)
    kurskod = Column(String)
    modulnamn = Column(String)
    poang = Column(Float)