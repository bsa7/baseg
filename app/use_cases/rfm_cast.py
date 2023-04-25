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

    # DATEDIFF('{self.__formatted_date(finish_date)}', MAX(rep_date)) AS r,
    # COUNT(*) AS f,
    # SUM(monetary) AS m,
    # COUNT(*) / DATEDIFF('{self.__formatted_date(finish_date)}', '{self.__formatted_date(start_date)}') AS k,
    # DATEDIFF(MAX(rep_date), MIN(rep_date)) AS d,
    # SUM(1 - DATEDIFF('{self.__formatted_date(finish_date)}', rep_date) / 90 * 0.025 * monetary) as i,

    # sql = f"""--beginsql
    #   SELECT
    #     client_id,
    #     ARRAY_AGG(DATEDIFF('{self.__formatted_date(finish_date)}', rep_date)) AS rep_dates,
    #     ARRAY_AGG(monetary) AS monetaries
    #   FROM replenishments
    #   WHERE rep_date >= '{self.__formatted_date(start_date)}'
    #     AND rep_date <= '{self.__formatted_date(finish_date)}'
    #   GROUP BY
    #     client_id
    # --endsql"""

    # sql = f"""--beginsql
    #   SELECT
    #     client_id,
    #     DATEDIFF(MAX(rep_date), MIN(rep_date)) AS d,
    #     SUM(1 - DATEDIFF('{self.__formatted_date(finish_date)}', rep_date) / 90 * 0.025 * monetary) as i,
    #     DATEDIFF('{self.__formatted_date(finish_date)}', MAX(rep_date)) AS r,
    #     COUNT(*) AS f,
    #     SUM(monetary) AS m
    #   FROM replenishments
    #   WHERE rep_date >= '{self.__formatted_date(start_date)}'
    #     AND rep_date <= '{self.__formatted_date(finish_date)}'
    #   GROUP BY
    #     client_id
    # --endsql"""

    sql = f"""--beginsql
      SELECT
        client_id,
        DATEDIFF(MAX(rep_date), MIN(rep_date)) AS d,
        SUM(1 - DATEDIFF('{self.__formatted_date(finish_date)}', rep_date) / 90 * 0.025 * monetary) as i,
        DATEDIFF('{self.__formatted_date(finish_date)}', MAX(rep_date)) AS r,
        COUNT(*) AS f,
        LOG(SUM(monetary)) AS m
      FROM replenishments
      WHERE rep_date >= '{self.__formatted_date(start_date)}'
        AND rep_date <= '{self.__formatted_date(finish_date)}'
        AND client_id != 23450
      GROUP BY
        client_id
    --endsql"""

    result = self.__spark.sql(sql)
    return result

  def __formatted_date(self, date: str):
    ''' Конвертирует дату в формате dd.mm.yyyy в формат sql yyyy-mm-dd '''
    parsed_date = parse_date(date)
    return timestamp_to_formatted_date(parsed_date)
