''' Этот файл содержит реализацию класса RfmCast '''
from app.lib.service_factory import ServiceFactory
from app.lib.utils import parse_date, timestamp_to_formatted_date

class RfmCast:
  ''' Этот класс создаёт дата фрейм с метками recency, frequency, monetary '''
  def __init__(self, source_dataframe):
    self.__df = source_dataframe
    self.__spark = ServiceFactory().spark('SparkWithSQL')

  def call(self, start_date: str, finish_date: str):
    ''' Этот метод возвращает датафрейм [client_id, recency, frequency, monetary] '''
    # Для вычисления разности дат, добавляем колонку `date` к исходному датафрейму
    df = self.__df

    print(df.tail(10))

    # Создаём датафрейм с признаком недавности (r), частоты (f) и денежности (m) клиента:
    # r - recency, высчитана в днях, разница между датой окончания интервала и датой транзакции;
    # f - frequency, количество пополнений (транзакций) за выбранный интервал времени;
    # m - monetary, нормализованное значение суммы пополнения баланса.
    # Дополнительно к rfm вводим ещё признаки
    # d - duration - продолжительность жизни клиента, вычисляется как разница между последней
    #     и первой транзакциями за агрегируемый интервал времени
    #  -

    df.createOrReplaceTempView('replenishments')

    sql = f"""--beginsql
      SELECT
        client_id,                                                                                         -- id клиента
        DATEDIFF(MAX(rep_date), MIN(rep_date)) + 1 AS client_lifetime,                                     -- Срок жизни клиента, дней
        SUM(1 - DATEDIFF('{self.__formatted_date(finish_date)}', rep_date) / 90 * 0.025 * monetary) as i,  -- Сумма пополнений с учётом коэффициента актуальности
        DATEDIFF('{self.__formatted_date(finish_date)}', MAX(rep_date)) AS recency,                        -- Дней с момента последнего пополнения
        COUNT(rep_date) AS frequency,                                                                      -- Количество пополнений
        SUM(monetary) AS monetary_sum,                                                                     -- monetary в нормализованном виде
        ROUND(SUM(monetary * 5e14), 2) AS absolute_monetary_sum,                                           -- monetary в рублях (умноженная на 5e14)
        ROUND(SUM(monetary * 5e14) / (DATEDIFF(MAX(rep_date), MIN(rep_date)) + 1), 2) AS monetary_per_day, -- monetary в рублях за день жизни клиента
        ROUND(SUM(monetary * 5e14) / COUNT(rep_date), 2) AS monetary_per_replenishment,                    -- monetary в рублях за одно пополнение
        COALESCE(ROUND(SQRT(VARIANCE(monetary)) * 5e14, 2), 0) AS standard_deviation,                      -- стандартное среднеквадратичное отклонение
        ROUND(AVG(monetary * 5e14), 2) AS monetary_average                                                 -- средняя monetary, руб.
      FROM replenishments
      WHERE rep_date >= '{self.__formatted_date(start_date)}'
        AND rep_date <= '{self.__formatted_date(finish_date)}'
      GROUP BY
        client_id
    --endsql"""

    return self.__spark.sql(sql)

  def __formatted_date(self, date: str):
    ''' Конвертирует дату в формате dd.mm.yyyy в формат sql yyyy-mm-dd '''
    parsed_date = parse_date(date)
    return timestamp_to_formatted_date(parsed_date)
