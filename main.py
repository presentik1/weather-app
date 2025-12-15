from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn

app = FastAPI(title="Погода онлайн")

# Шаблоны и статика
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = "372367ce6dbbcfa5a712232f20c1e54e"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/", response_class=templates.TemplateResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/weather")
def get_weather(city: str):
    """Возвращает JSON с погодой для JS"""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 404:
            return JSONResponse(content={"error": "Город не найден"}, status_code=404)
        if response.status_code == 401:
            return JSONResponse(content={"error": "Неверный API-ключ"}, status_code=401)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Ошибка запроса"}, status_code=response.status_code)

        data = response.json()

        weather = {
            "city": city.capitalize(),
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize()
        }
        return weather

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

