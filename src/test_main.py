import unittest
from main import get_weather
import unittest
import tkinter as tk
from main import AnalogClock


class TestWeatherFunction(unittest.TestCase):
    def test_get_weather_success(self):
        api_key = 'b571467ac02141716798e4555baa2768'
        result = get_weather(api_key, city="Riga")
        self.assertIn("°C", result)

    def test_get_weather_failure(self):
        api_key = '123'
        result = get_weather(api_key, city="Riga")
        self.assertEqual(result, "Weather data unavailable")


if __name__ == '__main__':
    unittest.main()


class TestAnalogClock(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.clock = AnalogClock(self.root, api_key="b571467ac02141716798e4555baa2768")

    def test_change_language_to_russian(self):
        self.clock.change_language('ru')
        self.assertEqual(self.clock.lang, 'ru')
        self.assertIn('Праздники в', self.clock.translations.get('holidays_title', ''))

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
