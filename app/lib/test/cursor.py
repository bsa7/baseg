''' Этот файл содержит определение класса Cursor, используемого в тестировочном клиенте MongoDB '''

class Cursor:
  ''' Этот класс эмулирует курсор MongoDB с результатами поиска в коллекции '''
  def __init__(self, results = None):
    self.__results = results or []

  def sort(self, _rules):
    ''' Сортирует (или нет) результаты на основе заданного правила '''
    # По факту пока не сортирует, но в тестах это пока не нужно
    return Cursor(self.__results)

  def limit(self, count):
    ''' Возвращает первые count элементов из выборки '''
    return Cursor(self.__results[:count])

  def next(self):
    ''' Возвращает следующий доступный элемент из результатов поиска, элементы берутся с конца списка '''
    return self.__results.pop()
