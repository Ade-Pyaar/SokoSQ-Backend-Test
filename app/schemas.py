from pydantic import BaseModel

from datetime import date


class WeatherSchema(BaseModel):
    city: str
    date: date
    temperature: float
    description: str
