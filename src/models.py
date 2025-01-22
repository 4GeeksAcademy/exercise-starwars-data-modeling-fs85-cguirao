import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla intermedia para indicar favoritos
favorites_table = Table(
    'favorites',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('usuario.id'), nullable=False),
    Column('character_id', Integer, ForeignKey('character.id'), nullable=True),
    Column('film_id', Integer, ForeignKey('film.episode_id'), nullable=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), nullable=True),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), nullable=True),
    Column('starship_id', Integer, ForeignKey('starship.id'), nullable=True),
    Column('specie_id', Integer, ForeignKey('specie.id'), nullable=True)
)

# Tabla intermedia para Character y Film
character_film = Table(
    'character_film',
    Base.metadata,
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True),
    Column('film_id', Integer, ForeignKey('film.episode_id'), primary_key=True)
)

# Tabla intermedia para Film y Planet
film_planet = Table(
    'film_planet',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('film.episode_id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

# Tabla intermedia para Film y Vehicle
film_vehicle = Table(
    'film_vehicle',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('film.episode_id'), primary_key=True),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True)
)

# Tabla intermedia para Film y Starship
film_starship = Table(
    'film_starship',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('film.episode_id'), primary_key=True),
    Column('starship_id', Integer, ForeignKey('starship.id'), primary_key=True)
)

# Tabla intermedia para Film y Specie
film_specie = Table(
    'film_specie',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('film.episode_id'), primary_key=True),
    Column('specie_id', Integer, ForeignKey('specie.id'), primary_key=True)
)

# Clases principales (sin cambios significativos)
class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    height = Column(String(10), nullable=False)
    mass = Column(String(30), nullable=False)
    hair_color = Column(String(10), nullable=False)
    skin_color = Column(String(10), nullable=False)
    eye_color = Column(String(10), nullable=False)
    birth_year = Column(String(10), nullable=False)
    gender = Column(String(30), nullable=False)
    homeworld_id = Column(Integer, ForeignKey('planet.id'), nullable=False)
    homeworld = relationship('Planet', back_populates='residents')
    specie_id = Column(Integer, ForeignKey('specie.id'), nullable=True)
    specie = relationship('Specie', back_populates='people')
    films = relationship('Film', secondary=character_film, back_populates='characters')

class Film(Base):
    __tablename__ = 'film'
    episode_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    opening_crawl = Column(String, nullable=False)
    director = Column(String, nullable=False)
    producer = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    characters = relationship('Character', secondary=character_film, back_populates='films')
    planets = relationship('Planet', secondary=film_planet, back_populates='films')
    vehicles = relationship('Vehicle', secondary=film_vehicle, back_populates='films')
    starships = relationship('Starship', secondary=film_starship, back_populates='films')
    species = relationship('Specie', secondary=film_specie, back_populates='films')

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    rotation_period = Column(Integer, nullable=False)
    orbital_period = Column(Integer, nullable=False)
    diameter = Column(Integer, nullable=False)
    climate = Column(String(30), nullable=False)
    gravity = Column(String(20), nullable=False)
    terrain = Column(String(10), nullable=False)
    surface_water = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    residents = relationship('Character', back_populates='homeworld')
    films = relationship('Film', secondary=film_planet, back_populates='planets')

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    model = Column(String(50), nullable=False)
    manufacturer = Column(String, nullable=False)
    cost_in_credits = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    max_atmosphering_speed = Column(Integer, nullable=False)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    cargo_capacity = Column(Integer, nullable=False)
    consumables = Column(String(20), nullable=False)
    vehicle_class = Column(String(50), nullable=False)
    films = relationship('Film', secondary=film_vehicle, back_populates='vehicles')

class Starship(Base):
    __tablename__ = 'starship'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    model = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    cost_in_credits = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    max_atmosphering_speed = Column(Integer, nullable=False)
    crew = Column(Integer, nullable=False)
    passengers = Column(Integer, nullable=False)
    cargo_capacity = Column(Integer, nullable=False)
    consumables = Column(String(30), nullable=False)
    hyperdrive_rating = Column(Integer, nullable=False)
    MGLT = Column(Integer, nullable=False)
    starship_class = Column(String(50), nullable=False)
    films = relationship('Film', secondary=film_starship, back_populates='starships')

class Specie(Base):
    __tablename__ = 'specie'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    classification = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    average_height = Column(Integer, nullable=False)
    skin_colors = Column(String, nullable=False)
    hair_colors = Column(String, nullable=False)
    eye_colors = Column(String, nullable=False)
    average_lifespan = Column(Integer, nullable=False)
    homeworld = Column(String, nullable=False)
    language = Column(String, nullable=False)
    people = relationship('Character', back_populates='specie')
    films = relationship('Film', secondary=film_specie, back_populates='species')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(50))
    password = Column(String(50))
    favorites = relationship('favorites', back_populates='user')

render_er(Base, 'diagram.png')
