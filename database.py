import datetime
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Targets the database running inside your Docker container
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PlayerStat(Base):
    __tablename__ = "player_stats"

    account_id = Column(String, primary_key=True, index=True)
    total_matches = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)

    unscored = Column(Integer)
    win_rate = Column(Float)
    # Keep the existing database column name so current PostgreSQL tables remain compatible.
    kill_death_ratio = Column("avg_kills", Float)
    avg_souls = Column(Integer)
    dominant_hero = Column(String)
    dominant_hero_matches = Column(Integer)
    overall_hero = Column(String)
    overall_hero_matches = Column(Integer)
    season = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS wins INTEGER"))
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS losses INTEGER"))
      
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS unscored INTEGER"))
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS dominant_hero_matches INTEGER"))
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS overall_hero VARCHAR"))
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS overall_hero_matches INTEGER"))
        connection.execute(text("ALTER TABLE player_stats ADD COLUMN IF NOT EXISTS season VARCHAR"))
