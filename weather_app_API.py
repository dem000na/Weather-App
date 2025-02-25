import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class WeatherApp(QWidget):
    # HTML stuff
    def __init__(self):
        super().__init__()

        self.text = QLabel("Enter city name:", self)
        self.city_name = QLineEdit(self)
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.temperature = QLabel(self)
        self.emoji_weather = QLabel(self)
        self.weather = QLabel(self)


        self.initUI()

    # CSS stuff
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 300, 300, 400)


        vbox = QVBoxLayout()

        vbox.addWidget(self.text)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.get_weather_btn)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji_weather)
        vbox.addWidget(self.weather)

        self.setLayout(vbox)

        self.text.setAlignment(Qt.AlignCenter)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji_weather.setAlignment(Qt.AlignCenter)
        self.weather.setAlignment(Qt.AlignCenter)

        self.get_weather_btn.clicked.connect(self.get_weather)

        self.city_name.setPlaceholderText("Enter a city")

        self.text.setStyleSheet("font-size: 30px")
        self.city_name.setStyleSheet("font-size: 25px")
        self.get_weather_btn.setStyleSheet("font-size: 25px")
        self.temperature.setStyleSheet("font-size: 30px")
        self.emoji_weather.setStyleSheet("font-size: 30px")
        self.weather.setStyleSheet("font-size: 30px")

    # Main Stuff
    def get_weather(self):
        # Getting API
        load_dotenv()
        API_key = os.getenv("API_key")
        city_name = self.city_name.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"

        # Request and error handling
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease chek your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbiden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Iternal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 503:
                    self.display_error("Gateway timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HHTP error occrued:\n{http_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n The request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature.setText(message)
        self.emoji_weather.setText("")
        self.weather.setText("")

    def display_weather(self, data):
        self.temperature.setText(f"{round(data["main"]["temp"])}°C")
        self.emoji_weather.setText(f"{self.get_emoji(data["weather"][0]["id"])}")
        self.weather.setText(f"{data["weather"][0]["description"]}")

    # Emoji for every weather
    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id < 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        



def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()