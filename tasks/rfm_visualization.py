# Этот скрипт загружает информацию о пополнениях баланса клиентами в Apache Spark дата фрейм
# На основании исходных данных составляется новый дата фрейм с признаками по клиентам:
# client_id; recency; frequency; monetary
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
#   * sample_size - количество точек в итоговой визуализации (если все комп не тянет)
#   * feature1 - признак 1 (из списка r, f, m, i, d)
#   * feature2 - признак 1 (из списка r, f, m, i, d)
#   * feature3 - признак 1 (из списка r, f, m, i, d)
# Пример запуска:
# Обратите внимание, что для файлов используется папка ../data - снаружи текущего репозитория
# python -m tasks.rfm_visualization input_file=../baseg-shared/result.parquet sample_size=100000 feature1=r feature2=f feature3=m
# или
# ./docker/run "python -m tasks.rfm_visualization input_file=../baseg-shared/result.parquet"

import pdb
import matplotlib.pyplot as plt
from pyspark.sql import functions as sql_functions
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

print(f'{argument_parser.arguments=}')

input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
sample_size = argument_parser.argument_safe('sample_size')
feature1 = argument_parser.argument_safe('feature1')
feature2 = argument_parser.argument_safe('feature2')
feature3 = argument_parser.argument_safe('feature3')

print(f'=============== Обрабатывается файл {input_file_name} ===============')

spark = ServiceFactory().spark('RMFCast')
df = Parquet().read_to_spark_df(input_file_name, spark).withColumnRenamed('partner', 'client_id')

plt_df = df.filter(df.absolute_monetary_sum < 1e7).toPandas()

if sample_size is not None:
  plt_df = plt_df.sample(n = int(sample_size))

fig = plt.figure()
axs = fig.add_subplot(projection = '3d')

axs.scatter(plt_df[feature1], plt_df[feature2], plt_df[feature3])
axs.set_xlabel(feature1)
axs.set_ylabel(feature2)
axs.set_zlabel(feature3)
axs.set_title(f'{feature1} / {feature2} / {feature3}')
print('======================')
plt.show()

# Завершаем сессию Apache Spark
spark.stop()
