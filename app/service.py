from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Weather
from app.schemas import WeatherSchema


def create_weather(db: Session, weather: WeatherSchema):

    try:
        get_weather_by_city(db, weather.city)
    except HTTPException:

        # there is no city with that name, create a new one
        db_weather = Weather(**weather.model_dump())
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
        return db_weather

    # there is a city with the name
    raise HTTPException(status_code=400, detail="City already exist")


def get_weather_by_city(db: Session, city: str):
    city = db.query(Weather).filter(Weather.city == city).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city
