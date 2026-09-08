import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime


# ============================================================
# LOAD API KEY FROM .env
# ============================================================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OpenWeather API key not found.\n\n"
        "Please make sure your .env file contains:\n\n"
        "OPENWEATHER_API_KEY=YOUR_API_KEY"
    )


# ============================================================
# WEATHER APPLICATION
# ============================================================

class WeatherApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced Weather App")

        # Use the available screen space
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.root.minsize(900, 650)

        self.unit = "metric"
        self.weather_icon = None

        self.create_interface()


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        self.main_frame = tk.Frame(self.root)

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )


        # ====================================================
        # TITLE
        # ====================================================

        title = tk.Label(
            self.main_frame,
            text="🌤 Advanced Weather App",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=(5, 5))


        subtitle = tk.Label(
            self.main_frame,
            text="Real-Time Weather & Forecast Information",
            font=("Arial", 13)
        )

        subtitle.pack(pady=(0, 15))


        # ====================================================
        # SEARCH AREA
        # ====================================================

        search_frame = tk.Frame(
            self.main_frame
        )

        search_frame.pack(
            fill="x",
            pady=10
        )


        search_inner = tk.Frame(
            search_frame
        )

        search_inner.pack()


        city_label = tk.Label(
            search_inner,
            text="City:",
            font=("Arial", 13, "bold")
        )

        city_label.grid(
            row=0,
            column=0,
            padx=6
        )


        self.city_entry = tk.Entry(
            search_inner,
            width=30,
            font=("Arial", 13)
        )

        self.city_entry.grid(
            row=0,
            column=1,
            padx=6
        )


        self.city_entry.bind(
            "<Return>",
            lambda event: self.get_weather()
        )


        get_button = tk.Button(
            search_inner,
            text="Get Weather",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=4,
            command=self.get_weather
        )

        get_button.grid(
            row=0,
            column=2,
            padx=6
        )


        self.unit_button = tk.Button(
            search_inner,
            text="Switch to °F",
            font=("Arial", 11),
            padx=10,
            pady=4,
            command=self.toggle_unit
        )

        self.unit_button.grid(
            row=0,
            column=3,
            padx=6
        )


        # ====================================================
        # CURRENT WEATHER
        # ====================================================

        current_container = tk.Frame(
            self.main_frame
        )

        current_container.pack(
            fill="both",
            expand=True,
            pady=10
        )


        self.weather_frame = tk.LabelFrame(
            current_container,
            text="Current Weather",
            font=("Arial", 15, "bold"),
            padx=20,
            pady=10
        )

        self.weather_frame.pack(
            fill="both",
            expand=True
        )


        self.location_label = tk.Label(
            self.weather_frame,
            text="Enter a city",
            font=("Arial", 25, "bold")
        )

        self.location_label.pack(
            pady=(10, 5)
        )


        self.icon_label = tk.Label(
            self.weather_frame
        )

        self.icon_label.pack(
            pady=2
        )


        self.temperature_label = tk.Label(
            self.weather_frame,
            text="--",
            font=("Arial", 38, "bold")
        )

        self.temperature_label.pack(
            pady=2
        )


        self.condition_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Arial", 16)
        )

        self.condition_label.pack(
            pady=2
        )


        self.details_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Arial", 12),
            justify="center"
        )

        self.details_label.pack(
            pady=8
        )


        # ====================================================
        # FORECAST
        # ====================================================

        forecast_container = tk.Frame(
            self.main_frame
        )

        forecast_container.pack(
            fill="both",
            expand=True,
            pady=10
        )


        forecast_title = tk.Label(
            forecast_container,
            text="Weather Forecast",
            font=("Arial", 19, "bold")
        )

        forecast_title.pack(
            pady=(0, 8)
        )


        text_frame = tk.Frame(
            forecast_container
        )

        text_frame.pack(
            fill="both",
            expand=True
        )


        self.forecast_text = tk.Text(
            text_frame,
            font=("Consolas", 11),
            wrap="none",
            state="disabled"
        )

        self.forecast_text.pack(
            side="left",
            fill="both",
            expand=True
        )


        vertical_scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.forecast_text.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )


        self.forecast_text.config(
            yscrollcommand=vertical_scrollbar.set
        )


        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = tk.Label(
            self.main_frame,
            text="Ready — Enter a city to get weather information",
            font=("Arial", 10)
        )

        self.status_label.pack(
            pady=(5, 0)
        )


    # ========================================================
    # GET WEATHER
    # ========================================================

    def get_weather(self):

        city = self.city_entry.get().strip()


        if not city:

            messagebox.showwarning(
                "Input Required",
                "Please enter a city name."
            )

            return


        self.status_label.config(
            text="Fetching weather data..."
        )


        try:

            current_url = (
                "https://api.openweathermap.org/data/2.5/weather"
            )


            parameters = {
                "q": city,
                "appid": API_KEY,
                "units": self.unit
            }


            response = requests.get(
                current_url,
                params=parameters,
                timeout=10
            )


            if response.status_code == 401:

                messagebox.showerror(
                    "API Key Error",
                    "Your OpenWeather API key is invalid "
                    "or has not been activated yet."
                )

                self.status_label.config(
                    text="API key error."
                )

                return


            if response.status_code == 404:

                messagebox.showerror(
                    "City Not Found",
                    f"Could not find weather information for:\n\n{city}"
                )

                self.status_label.config(
                    text="City not found."
                )

                return


            response.raise_for_status()

            weather_data = response.json()


            self.display_weather(
                weather_data
            )


            latitude = weather_data["coord"]["lat"]
            longitude = weather_data["coord"]["lon"]


            self.get_forecast(
                latitude,
                longitude
            )


            self.status_label.config(
                text="Weather updated successfully."
            )


        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Connection Error",
                "Please check your internet connection."
            )


        except requests.exceptions.Timeout:

            messagebox.showerror(
                "Timeout Error",
                "The weather server took too long to respond."
            )


        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Weather Error",
                f"Unable to retrieve weather data.\n\n{error}"
            )


        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Something went wrong.\n\n{error}"
            )


    # ========================================================
    # DISPLAY CURRENT WEATHER
    # ========================================================

    def display_weather(self, data):

        city = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        condition = (
            data["weather"][0]["description"]
            .title()
        )

        wind_speed = data["wind"]["speed"]


        if self.unit == "metric":

            temperature_unit = "°C"
            wind_unit = "m/s"

        else:

            temperature_unit = "°F"
            wind_unit = "mph"


        self.location_label.config(
            text=f"{city}, {country}"
        )


        self.temperature_label.config(
            text=f"{temperature:.1f}{temperature_unit}"
        )


        self.condition_label.config(
            text=condition
        )


        details = (
            f"Feels Like: "
            f"{feels_like:.1f}{temperature_unit}\n"
            f"Humidity: {humidity}%\n"
            f"Pressure: {pressure} hPa\n"
            f"Wind Speed: {wind_speed:.1f} {wind_unit}"
        )


        self.details_label.config(
            text=details
        )


        # ====================================================
        # WEATHER ICON
        # ====================================================

        icon_code = data["weather"][0]["icon"]

        icon_url = (
            f"https://openweathermap.org/img/wn/"
            f"{icon_code}@2x.png"
        )


        try:

            icon_response = requests.get(
                icon_url,
                timeout=10
            )

            icon_response.raise_for_status()


            icon_image = Image.open(
                BytesIO(
                    icon_response.content
                )
            )


            icon_image = icon_image.resize(
                (110, 110)
            )


            self.weather_icon = ImageTk.PhotoImage(
                icon_image
            )


            self.icon_label.config(
                image=self.weather_icon
            )


        except Exception:

            self.icon_label.config(
                image=""
            )


    # ========================================================
    # GET FORECAST
    # ========================================================

    def get_forecast(
        self,
        latitude,
        longitude
    ):

        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
        )


        parameters = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": self.unit
        }


        try:

            response = requests.get(
                forecast_url,
                params=parameters,
                timeout=10
            )


            response.raise_for_status()

            forecast_data = response.json()


            self.display_forecast(
                forecast_data
            )


        except requests.exceptions.RequestException:

            self.forecast_text.config(
                state="normal"
            )


            self.forecast_text.delete(
                "1.0",
                tk.END
            )


            self.forecast_text.insert(
                tk.END,
                "Forecast information could not be loaded."
            )


            self.forecast_text.config(
                state="disabled"
            )


    # ========================================================
    # DISPLAY FORECAST
    # ========================================================

    def display_forecast(self, data):

        self.forecast_text.config(
            state="normal"
        )


        self.forecast_text.delete(
            "1.0",
            tk.END
        )


        if self.unit == "metric":

            temperature_unit = "°C"

        else:

            temperature_unit = "°F"


        forecasts = data["list"]


        # ====================================================
        # NEXT 6 HOURS
        # ====================================================

        self.forecast_text.insert(
            tk.END,
            "NEXT 6 HOURS\n"
        )


        self.forecast_text.insert(
            tk.END,
            "=" * 90 + "\n"
        )


        for item in forecasts[:2]:

            forecast_time = datetime.fromtimestamp(
                item["dt"]
            ).strftime(
                "%d %b %I:%M %p"
            )


            temperature = item["main"]["temp"]


            condition = (
                item["weather"][0]["description"]
                .title()
            )


            humidity = item["main"]["humidity"]


            self.forecast_text.insert(
                tk.END,
                f"{forecast_time:<25}"
                f"{temperature:.1f}{temperature_unit:<10}"
                f"{condition:<25}"
                f"Humidity: {humidity}%\n"
            )


        # ====================================================
        # NEXT 5 DAYS
        # ====================================================

        self.forecast_text.insert(
            tk.END,
            "\nNEXT 5 DAYS\n"
        )


        self.forecast_text.insert(
            tk.END,
            "=" * 90 + "\n"
        )


        daily_data = {}


        for item in forecasts:

            date = datetime.fromtimestamp(
                item["dt"]
            ).strftime(
                "%Y-%m-%d"
            )


            if date not in daily_data:

                daily_data[date] = item


        count = 0


        for date, item in daily_data.items():

            if count >= 5:

                break


            readable_date = datetime.strptime(
                date,
                "%Y-%m-%d"
            ).strftime(
                "%A, %d %b"
            )


            temperature = item["main"]["temp"]


            condition = (
                item["weather"][0]["description"]
                .title()
            )


            humidity = item["main"]["humidity"]


            self.forecast_text.insert(
                tk.END,
                f"{readable_date:<25}"
                f"{temperature:.1f}{temperature_unit:<10}"
                f"{condition:<25}"
                f"Humidity: {humidity}%\n"
            )


            count += 1


        self.forecast_text.config(
            state="disabled"
        )


    # ========================================================
    # CELSIUS / FAHRENHEIT
    # ========================================================

    def toggle_unit(self):

        if self.unit == "metric":

            self.unit = "imperial"

            self.unit_button.config(
                text="Switch to °C"
            )

        else:

            self.unit = "metric"

            self.unit_button.config(
                text="Switch to °F"
            )


        if self.city_entry.get().strip():

            self.get_weather()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()
