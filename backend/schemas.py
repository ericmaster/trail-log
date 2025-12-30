from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class SessionTypeEnum(str, Enum):
    race = "race"
    training = "training"
    recovery = "recovery"


class HydrationStatusEnum(str, Enum):
    well_hydrated = "well_hydrated"
    mildly_dehydrated = "mildly_dehydrated"
    uncertain = "uncertain"


class WeatherConditionEnum(str, Enum):
    sunny = "sunny"
    cloudy = "cloudy"
    rain = "rain"
    fog = "fog"
    snow = "snow"
    windy = "windy"


class TrailConditionEnum(str, Enum):
    dry = "dry"
    muddy = "muddy"
    icy = "icy"
    rocky = "rocky"
    mixed = "mixed"


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    body_weight: Optional[float] = None
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[GenderEnum] = None
    vo2max: Optional[float] = None


class UserResponse(BaseModel):
    id: int
    email: str
    body_weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    vo2max: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Upload schemas
class UploadMetadata(BaseModel):
    session_type: Optional[SessionTypeEnum] = None
    race_name: Optional[str] = None
    notes: Optional[str] = None
    fatigue_level: Optional[int] = Field(None, ge=1, le=5)
    sleep_quality: Optional[int] = Field(None, ge=1, le=5)
    hydration_status: Optional[HydrationStatusEnum] = None
    weather_condition: Optional[WeatherConditionEnum] = None
    trail_condition: Optional[TrailConditionEnum] = None


class UploadResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    upload_date: datetime
    session_type: Optional[SessionTypeEnum] = None
    race_name: Optional[str] = None
    notes: Optional[str] = None
    fatigue_level: Optional[int] = None
    sleep_quality: Optional[int] = None
    hydration_status: Optional[HydrationStatusEnum] = None
    weather_condition: Optional[WeatherConditionEnum] = None
    trail_condition: Optional[TrailConditionEnum] = None

    class Config:
        from_attributes = True
