import pyowm

class Weather:
    def __init__(self, api_key):
        self.owm = pyowm.OWM(api_key)

    def get_weather_at_place(self, place):
        observation = self.owm.weather_at_place(place)
        w = observation.get_weather()
        return w.get_detailed_status(), w.get_temperature('celsius')['temp']

    def speak_weather(self, place):
        try:
            status, temperature = self.get_weather_at_place(place)
            print(f"Current weather in {place} is {status} with a temperature of {temperature} degrees Celsius.")
        except pyowm.exceptions.api_response_error.NotFoundError:
            print(f"Sorry, I couldn't find the weather for {place}.")
