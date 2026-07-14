from sqlalchemy import Column, Integer, String
from .database import Base
class Vaga(Base):
    __tablename__ = 'vagas'

    id = Column(Integer, primary_key=True)
    titulo = Column(String) 
    empresa = Column(String)
    formato = Column(String)
    link = Column(String)
    nivel = Column(String)