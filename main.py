import flet as ft
import requests
from api_key import API_KEY

# Build out the API and get a response
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
MAP_URL = "https://www.openstreetmap.org/export/embed.html?bbox={lon}%2C{lat}%2C{lon}%2C{lat}&layer=mapnik"

def get_weather(city):
    params = { "q": city, "appid": API_KEY, "units": "metric" }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
      data = response.json()
      return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
      }
    return None


def main(page: ft.Page):
  page.title = "Flet My Weather App"
  page.bgcolor = ft.Colors.BLUE_GREY_900
  page.padding = 20
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.window_width = 500
  page.window_height = 700

  city_input = ft.TextField(
    label="Enter a city",
    width=300,
    bgcolor=ft.Colors.WHITE,
    color=ft.Colors.BLACK,
    border_radius=10
  )

  results_text = ft.Text("", size=18,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)

  # Create a map
  map_frame = ft.WebView(url="",width=600,height=400,visible=False)

  # Call the search
  def search_weather(e):
    results_text.value = ""
    page.update()
    city = city_input.value.strip()
    if not city:
      results_text.value = "Please enter a city name..."
      page.update()
      return
    weather_data = get_weather(city)

    if weather_data:
      results_text.value = f"City: {weather_data['city']}\nTemperature: {weather_data['temp']}°C\nHumidity: {weather_data['humidity']}%\nWeather: {weather_data['weather']}"
      map_frame.url = MAP_URL.format(lat=weather_data['lat'], lon=weather_data['lon'])
      map_frame.visible = True
    else:
      results_text.value = "City not found. Try again..."
      map_frame.visible = False
    page.update()

  search_button = ft.ElevatedButton(
    "Search",
    on_click=search_weather,
    bgcolor=ft.Colors.BLUE_GREY_500,
    color=ft.Colors.WHITE,
    style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=10),
      padding=10
    )
  )

  container = ft.Container(
    content=ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text("Flet My Weather App", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        city_input,
        search_button,
        results_text,
        map_frame
      ]
    ),
    alignment=ft.alignment.center,
    padding=20,
    border_radius=15,
    bgcolor=ft.Colors.BLUE_GREY_800,
    shadow=ft.BoxShadow(blur_radius=15,spread_radius=2,color=ft.Colors.BLACK12)
  )
  
  page.add(container)


if __name__ == "__main__":
  ft.app(target=main)