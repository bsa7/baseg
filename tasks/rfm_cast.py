# Этот скрипт загружает информацию о пополнениях баланса клиентами в Apache Spark дата фрейм
# На основании исходных данных составляется новый дата фрейм с признаками по клиентам:
# client_id; recency; frequency; monetary
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
#   * target_date - дата, на которую нужно посчитать метрики R, F, M. Формат даты = дд.мм.гггг
#   * output_file - путь к файлу, в который будет записан датафрейм с признаками.
# Пример запуска:
# Обратите внимание, что для файлов используется папка ../data - снаружи текущего репозитория
# python -m tasks.parquet_info_with_spark input_file=../data/data.parquet.gzip target_date=23.03.2023 output_file=../data/result.parquet

from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.use_cases.rfm_cast import RfmCast
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

print(f'{argument_parser.arguments=}')

# Парсим аргументы, переданные в командной строке
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
target_date = argument_parser.argument_safe('target_date', 'Ошибка! Вы должны указать дату, на которую нужно найти признаки')
output_file_name = argument_parser.argument_safe('output_file', 'Ошибка! Вы должны указать имя результирующего файла!')

print(f'=============== Обрабатывается файл {input_file_name} ===============')

# Загружаем данные о пополнении баланса в датафрейм:
spark = ServiceFactory().spark('RMFCast')
df = Parquet().read_to_spark_df(input_file_name, spark).withColumnRenamed('partner', 'client_id')

# Создаём датафрейм с признаками на дату target_date
recency_df = RfmCast(df).call(target_date)

recency_df.show(20)
print(f'Всего уникальных клиентов: {recency_df.count()}')

# Пишем результат в указанный файл output_file
Parquet().write(recency_df.toPandas(), output_file_name)
print(f'Итоговый датафрейм сохранён в файле {output_file_name}')

# Завершаем сессию Apache Spark
spark.stop()
