''' Этот файл содержит определение абстрактного класса Singleton '''

class Singleton(type):
  ''' Класс, у которого может быть создан только один экземпляр (гугли паттерн Singleton) '''
  instance = None

  def __call__(cls, *args, **kwargs):
    if cls.instance is None:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance
