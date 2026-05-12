import requests
from pprint import pprint
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    token = 'b1e619da98974045a4d192102231911'  # Вставить ваш токен из api.weatherapi.com
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json()

    # Данная реализация приведена для api.weatherapi.com
    result = {
        'city': data['location']['name'],  # Город
        'time': data['current']['last_updated'],  # Время обновления данных
        'temp': data['current']['temp_c'],  # Температура
        'feels_like_temp': data['current']['feelslike_c'],  # Ощущаемая температура
        'pressure': data['current']['pressure_mb'],  # Давление
        'humidity': data['current']['humidity'],  # Влажность
        'wind_speed': data['current']['wind_kph'],  # Скорость ветра
        'wind_gust': data['current']['gust_kph'],  # Порывы ветра
        'wind_dir': DIRECTION_TRANSFORM.get(data['current']['wind_dir'].lower()),  # Направление ветра
    }
    return result


if __name__ == "__main__":
    pprint(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
