import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'gear.db')}"

Base = declarative_base()
# Gear inventory table
class Gear(Base):
    __tablename__ = 'gear'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)
    weight_grams = Column(Float)
    status = Column(String, default="owned")  # e.g., owned, wishlist, ordered
    notes = Column(String, nullable=True)
    link = Column(String, nullable=True)
    image_path = Column(String)# path to image file

# Maintenance reminders table
class Maintenance(Base):
    __tablename__ = 'maintenance'
    id = Column(Integer, primary_key=True)
    gear_id = Column(Integer, ForeignKey('gear.id'))
    description = Column(String)
    interval_days = Column(Integer)
    last_done = Column(Date, default=datetime.date.today)

    gear = relationship("Gear")

# Wishlist table
class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gear_id = Column(Integer, ForeignKey("gear.id"), nullable=False)
    target_price = Column(Float, nullable=False)

    gear = relationship("Gear")  # Relationship to Gear table

# Trips table
class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)

# Gear used in trips
class TripGear(Base):
    __tablename__ = 'trip_gear'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    gear_id = Column(Integer, ForeignKey('gear.id'))
    used = Column(Boolean, default=True)
    feedback = Column(String, nullable=True)

    gear = relationship("Gear")
    trip = relationship("Trip")

def setup_db():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    print("Database schema created successfully.")

if __name__ == "__main__":
    setup_db()
