from pydantic import BaseModel, ConfigDict  

class VagaBase(BaseModel):
    titulo: str
    empresa: str
    formato: str
    link: str
    nivel: str

class Vaga(VagaBase): #Colocando na classe Vaga pois ela já possui o campos completos
    id: int

    model_config = ConfigDict(from_attributes=True) #Colocando para ler atributos de orm_mode ao invez de ler apenas chaves de dicionário
