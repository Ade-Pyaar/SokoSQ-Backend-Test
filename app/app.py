from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session


from app import service, models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/weather/",
    response_model=schemas.WeatherSchema,
    status_code=status.HTTP_201_CREATED,
)
def add_weather_data(weather: schemas.WeatherSchema, db: Session = Depends(get_db)):
    return service.create_weather(db=db, weather=weather)


@app.get("/weather/{city}", response_model=schemas.WeatherSchema)
def get_weather_data(city: str, db: Session = Depends(get_db)):
    return service.get_weather_by_city(db=db, city=city)
