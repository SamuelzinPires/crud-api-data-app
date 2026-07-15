from sqlalchemy import Column, Integer, String  # import de variáveis, para definir os tipos de dados
from .database import Base  # importa a classe Base do arquivo database.py, que é usada como base para definir os modelos de banco de dados
class Vaga(Base):   # classe que representa a tabela "vagas" no banco de dados
    __tablename__ = 'vagas'   # nome da tabela no banco de dados

    id = Column(Integer, primary_key=True)
    titulo = Column(String) 
    empresa = Column(String)
    formato = Column(String)
    link = Column(String)
    nivel = Column(String)