''' Этот файл содержит код, который по parquet-файлу с данными строит датафрейм с историей пополнений для каждого клиента '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python -m tasks.client_behaviour_to_df input_file=../baseg-shared/data/wallet_urfu.parquet.gzip start_date=23.03.2021 finish_date=23.03.2023 output_file=../baseg-shared/data/behaviour.parquet

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import sys
from datetime import date
# from tslearn.clustering import TimeSeriesKMeans

from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet
from app.lib.utils import parse_date, timestamp_to_formatted_date

argument_parser = ArgumentParser()
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
output_file_name = argument_parser.argument_safe('output_file', 'Ошибка! Вы должны указать имя результирующего файла!')
start_date = argument_parser.argument_safe('start_date', 'Ошибка! Вы должны указать дату в формате dd.mm.yyyy, начиная с которой нужно найти признаки')
finish_date = argument_parser.argument_safe('finish_date', 'Ошибка! Вы должны указать дату в формате dd.mm.yyyy, на которую нужно найти признаки')
monetary_const = argument_parser.argument_safe('monetary_const', default = 5e14)
spark = ServiceFactory().spark('ClientBehaviourToDf')
df = Parquet().read_to_spark_df(input_file_name, spark)
df.createOrReplaceTempView('replenishments')

def formatted_date(date: str):
  ''' Конвертирует дату в формате dd.mm.yyyy в формат sql yyyy-mm-dd '''
  parsed_date = parse_date(date)
  return timestamp_to_formatted_date(parsed_date)

def filter_sql(start_date: str, finish_date: str, monetary_const: float):
  return f"""--beginsql
    SELECT
      client_id,
      ARRAY_AGG(rep_day) AS rep_indices,
      ARRAY_AGG(per_day_monetary) AS rep_values
    FROM (
      SELECT
        partner AS client_id,
        DATEDIFF(day, '{formatted_date(start_date)}', rep_date) AS rep_day,
        SUM(monetary * {monetary_const}) AS per_day_monetary
      FROM replenishments
      WHERE rep_date >= '{formatted_date(start_date)}'
        AND rep_date <= '{formatted_date(finish_date)}'
      GROUP BY
        client_id,
        rep_date
      ORDER BY
        client_id,
        rep_date
    )
    GROUP BY
      client_id
  --endsql"""

sql = filter_sql(start_date, finish_date, monetary_const=monetary_const)
filtered_df = spark.sql(sql)

print(f'Генерация датасета с историей пополнений в файл {output_file_name}')
filtered_df.write.parquet(output_file_name, mode='overwrite', compression='gzip')

# Результат будет сохранён в виде:
#    client_id                                        rep_indices                                         rep_values
# 0          0  [4, 24, 53, 85, 112, 115, 158, 177, 189, 238, ...  [4.585403974388945e-12, 2.0735200089818858e-13...
# 1         19                         [22, 46, 57, 88, 115, 143]  [1.4187242166718167e-10, 3.273978961550346e-11...
# 2         26                                         [445, 599]     [1.091326320516782e-12, 1.091326320516782e-12]
# 3         29  [11, 79, 92, 94, 169, 218, 281, 415, 466, 536,...  [9.797531117614793e-10, 1.1065167098373193e-10...
# 4         54  [3, 18, 32, 64, 80, 95, 109, 123, 136, 156, 18...  [3.1313447941114434e-11, 3.3212508524498516e-1...
