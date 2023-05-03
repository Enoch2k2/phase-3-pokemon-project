from sqlalchemy import Table, Column, String, Integer, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from query_methods import _find_by_name, _all

Base = declarative_base()

trainer_pokemons = Table(
    "trainer_pokemons",
    Base.metadata,
    Column('trainer_id', ForeignKey('trainers.id'), primary_key=True),
    Column('pokemon_id', ForeignKey('pokemons.id'), primary_key=True),
    extend_existing=True,
)


class Trainer(Base):
    __tablename__ = "trainers"

    Index("index_name", "name")

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    pokemons = relationship(
        "Pokemon", secondary=trainer_pokemons, back_populates="trainers")

    def __repr__(self):
        return f'Trainer {self.id}: ' \
            + f'{self.name}'

    def catch_pokemon(self, session, pokemon):
        self.pokemons.append(pokemon)
        session.commit()

    def sorted_pokemons(self):
        return sorted(
            self.pokemons, key=lambda pokemon: pokemon.pokedex_id)

    @classmethod
    def find_by_name(self, session, name):
        return _find_by_name(self, session, name)

    @classmethod
    def all(self, session):
        return _all(self, session)


class Pokemon(Base):
    __tablename__ = "pokemons"

    Index("index_name", "name")

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    pokedex_id = Column(Integer())

    trainers = relationship(
        "Trainer", secondary=trainer_pokemons, back_populates="pokemons")

    def __repr__(self):
        return f"Pokemon {self.id}: " \
            + f"{self.name}, " \
            + f"Pokedex Id {self.pokedex_id}"

    @classmethod
    def find_by_name(self, session, name):
        return _find_by_name(self, session, name)

    @classmethod
    def all(self, session):
        return _all(self, session)
