from sqlalchemy import Column, Integer, String,BOOLEAN, create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Pokemon(Base):
    __tablename__ = 'Pokemon'  # Ensure this matches the table name in your database

    Id = Column(Integer, primary_key=True)
    DexNumber = Column(Integer)
    Name = Column(String)
    Form = Column(String)
    Type1 = Column(String)
    Type2 = Column(String)
    Total = Column(Integer)
    Hp = Column(Integer)
    Attack = Column(Integer)
    Defense = Column(Integer)
    SpecialAttack = Column(Integer)
    SpecialDefense = Column(Integer)
    Speed = Column(Integer)
    Generation = Column(Integer)
    
    
    def __repr__(self):
        return (f"ID: {self.Id} | DexNumber: {self.DexNumber}, Name: {self.Name}, Form: {self.Form}, "
                f"Type1: {self.Type1}, Type2: {self.Type2}, Total: {self.Total}, HP: {self.Hp}, "
                f"Attack: {self.Attack}, Defense: {self.Defense}, SpecialAttack: {self.SpecialAttack}, "
                f"SpecialDefense: {self.SpecialDefense}, Speed: {self.Speed}, Generation: {self.Generation}")
    
class PokemonType(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class PokemonSpecies(Base):
    __tablename__ = "pokemon_species"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    is_legendary = Column(BOOLEAN)
    is_mythical = Column(BOOLEAN)
    capture_rate = Column(Integer)
    generation = Column(String(50))
    
    def __repr__(self):
        return f"<PokemonSpecies(name='{self.name}', id={self.id}, is_legendary={self.is_legendary}, is_mythical={self.is_mythical}, capture_rate={self.capture_rate})>"



