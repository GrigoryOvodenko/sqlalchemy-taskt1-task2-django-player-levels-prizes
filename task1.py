from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class BoostType(enum.Enum):
    LEVEL_UP = "Level Up"
    MANUAL = "Manual"


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_login = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    points = Column(Integer, default=0)

    boosts = relationship("PlayerBoost", back_populates="player")


class Boost(Base):
    __tablename__ = "boosts"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(BoostType), nullable=False)
    description = Column(String)

    player_boosts = relationship("PlayerBoost", back_populates="boost")


class PlayerBoost(Base):
    __tablename__ = "player_boosts"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    boost_id = Column(Integer, ForeignKey("boosts.id"), nullable=False)
    date_received = Column(DateTime, default=datetime.utcnow)
    method = Column(Enum(BoostType), nullable=False)

    player = relationship("Player", back_populates="boosts")

    boost = relationship("Boost", back_populates="player_boosts")
