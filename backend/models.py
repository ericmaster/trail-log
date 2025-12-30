from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class SessionTypeEnum(str, enum.Enum):
    race = "race"
    training = "training"
    recovery = "recovery"


class HydrationStatusEnum(str, enum.Enum):
    well_hydrated = "well_hydrated"
    mildly_dehydrated = "mildly_dehydrated"
    uncertain = "uncertain"


class WeatherConditionEnum(str, enum.Enum):
    sunny = "sunny"
    cloudy = "cloudy"
    rain = "rain"
    fog = "fog"
    snow = "snow"
    windy = "windy"


class TrailConditionEnum(str, enum.Enum):
    dry = "dry"
    muddy = "muddy"
    icy = "icy"
    rocky = "rocky"
    mixed = "mixed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    body_weight = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    vo2max = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    uploads = relationship("Upload", back_populates="owner")


class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    # Session metadata
    session_type = Column(SQLEnum(SessionTypeEnum), nullable=True)
    race_name = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Physiological/Subjective
    fatigue_level = Column(Integer, nullable=True)  # 1-5
    sleep_quality = Column(Integer, nullable=True)  # 1-5
    hydration_status = Column(SQLEnum(HydrationStatusEnum), nullable=True)

    # Environmental
    weather_condition = Column(SQLEnum(WeatherConditionEnum), nullable=True)
    trail_condition = Column(SQLEnum(TrailConditionEnum), nullable=True)

    owner = relationship("User", back_populates="uploads")
