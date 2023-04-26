''' Этот файл содержит различные методы, используемые в коде приложения
    Если можно, то отсюда методы стоит выносить в отдельные модули по темам
'''
from datetime import datetime

def timestamp_to_formatted_datetime(timestamp: int, datetime_format = '%Y-%m-%d %H:%M:%S.%f') -> str:
  ''' Конвертирует Unix штамп времени с миллисекундами (1585557000000) в форматированную дату/время типа:
      2020-03-30 08:30:00.231000 '''
  return datetime.utcfromtimestamp(timestamp / 1000.0).strftime(datetime_format)

def timestamp_to_formatted_date(timestamp: int, date_format = '%Y-%m-%d') -> str:
  ''' Конвертирует Unix штамп времени с миллисекундами (1585557000000) в форматированную дату типа:
      2020-03-30 '''
  return datetime.utcfromtimestamp(timestamp / 1000.0).strftime(date_format)

def parse_date(date: str, date_format = '%d.%m.%Y'):
  ''' Парсит строку в заданном формате в unix timestamp (в миллисекундах) '''
  return datetime.strptime(date, date_format).timestamp() * 1000

def current_timestamp() -> int:
  ''' Этот метод возвращает текущее время в виде временного штампа Unix (в миллисекундах) '''
  return int(datetime.now().timestamp() * 1000)

def seconds(value: float) -> int:
  ''' Этот метод возвращает время в секундах, выраженное в миллисекундах '''
  return int(value * 1000)

def minutes(value: float) -> int:
  ''' Этот метод возвращает время в минутах, выраженное в миллисекундах '''
  return seconds(value * 60)

def hours(value: float) -> int:
  ''' Этот метод возвращает время в часах, выраженное в миллисекундах '''
  return minutes(value * 60)

def days(value: float) -> int:
  ''' Этот метод возвращает время в днях, выраженное в миллисекундах '''
  return hours(value * 24)

def filter_list(filter_attributes):
  ''' Этот метод возвращает лямбда-функцию для фильтрации списков '''
  def filter_lambda(item):
    ''' Фильтрует список по заданным значениям атрибутов '''
    return item.items() | filter_attributes.items() == item.items()

  return filter_lambda
