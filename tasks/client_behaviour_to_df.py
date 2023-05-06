''' Этот файл содержит код, который по parquet-файлу с данными строит датафрейм с историей пополнений для каждого клиента '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python -m tasks.client_behaviour_to_df input_file=../baseg-shared/data/wallet_urfu.parquet.gzip start_date=23.03.2021 finish_date=23.03.2023 output_file=../baseg-shared/data/behaviour.parquet

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import sys
from datetime import date
from tslearn.clustering import TimeSeriesKMeans

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
spark = ServiceFactory().spark('Visualize client behaviour')
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
      ARRAY_AGG(rep_date) AS rep_dates,
      ARRAY_AGG(per_day_monetary) AS per_day_monetaries,
      ARRAY_AGG(per_day_replenishment_count) AS per_day_replenishment_counts
    FROM (
      SELECT
        partner AS client_id,
        rep_date,
        SUM(monetary * {monetary_const}) AS per_day_monetary,
        COUNT(rep_date) AS per_day_replenishment_count
      FROM replenishments
      WHERE rep_date >= '{formatted_date(start_date)}'
        AND rep_date <= '{formatted_date(finish_date)}'
      GROUP BY
        client_id,
        rep_date
    )
    GROUP BY client_id
  --endsql"""

sql = filter_sql(start_date, finish_date, monetary_const=monetary_const)
filtered_df = spark.sql(sql)

start_date = date.fromtimestamp(parse_date(start_date) / 1000)
finish_date = date.fromtimestamp(parse_date(finish_date) / 1000)
interval_length = (finish_date - start_date).days
df = filtered_df.toPandas()
def interval_rep_days(client_id):
  ''' Даты пополнений заменяются на число дней от даты, до начала интервала '''
  cell = df[df['client_id'] == client_id].iloc[0]['rep_dates']
  return [(x - start_date).days for x in cell]

def interval_rep_items(client_id, column_name):
  ''' суммы пополнений, количество пополнений в день '''
  return df[df['client_id'] == client_id].iloc[0][column_name]

def client_behaviour(client_id):
  behaviour_df = np.zeros(interval_length)
  indices = interval_rep_days(client_id)
  monetaries = interval_rep_items(client_id, 'per_day_monetaries')
  behaviour_df[indices] = monetaries
  return behaviour_df

print(df)

print(f'Генерация датасета с историей пополнений в файл {output_file_name}')
behaviour_df = df[['client_id']]
behaviour_df['replenishments_by_day'] = df['client_id'].apply(client_behaviour)
behaviour_df.to_parquet(output_file_name, compression='gzip')
