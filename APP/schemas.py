from pydantic import BaseModel, ConfigDict, Field

class VagaBase(BaseModel):
    titulo: str = Field(min_length=1)
    empresa: str = Field(min_length=1)
    formato: str | None = Field(default=None)
    link: str = Field(min_length=1)
    nivel: str | None = Field(default=None)

class Vaga(VagaBase): #Colocando na classe Vaga pois ela já possui o campos completos
    id: int 

    model_config = ConfigDict(from_attributes=True) #Colocando para ler atributos de orm_mode ao invez de ler apenas chaves de dicionário

