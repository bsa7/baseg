''' Этот файл содержит реализацию класса RfmCast '''
from pyspark.sql import functions as sql_functions

class RfmCast:
  ''' Этот класс создаёт дата фрейм с метками recency, frequency, monetary '''
  def __init__(self, source_dataframe):
    self.__df = source_dataframe

  def call(self, start_date: str, finish_date: str):
    ''' Этот метод возвращает датафрейм [client_id, recency, frequency, monetary] '''
    # Для вычисления разности дат, добавляем колонку `date` к исходному датафрейму
    df = self.__df. \
      withColumn('start_date', sql_functions.to_date(sql_functions.lit(start_date), 'dd.MM.yyyy')). \
      withColumn('finish_date', sql_functions.to_date(sql_functions.lit(finish_date), 'dd.MM.yyyy'))

    # Создаём датафрейм с признаком недавности (r), частоты (f) и денежности (m) клиента:
    # r высчитана в днях, f - в количестве пополнений, m - в абстрактных еденицах суммы
    return df.filter((df.rep_date >= df.start_date) & (df.rep_date <= df.finish_date)) \
      .withColumn('date_diff', sql_functions.datediff('finish_date', 'rep_date')) \
      .groupBy('client_id') \
      .agg(
        sql_functions.min('date_diff').alias('r'), \
        sql_functions.count('date_diff').alias('f'), \
        sql_functions.sum('monetary').alias('m'))
