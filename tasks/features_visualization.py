# Этот скрипт загружает аггрегированную информацию из файла features.gz,parquet

# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
# Пример запуска:
# Обратите внимание, что для файлов используется папка ../data - снаружи текущего репозитория
# python -m tasks.features_visualization input_file=../baseg-shared/features.gz.parquet sample_size=100000
# или
# ./docker/run "python -m tasks.features_visualization input_file=../baseg-shared/features.gz.parquet sample_size=100000"

import matplotlib.pyplot as plt
from pyspark.sql import functions as sql_functions
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

print(f'{argument_parser.arguments=}')

input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
sample_size = argument_parser.argument_safe('sample_size')

print(f'=============== Обрабатывается файл {input_file_name} ===============')

spark = ServiceFactory().spark('RMFCast')
df = Parquet().read_to_spark_df(input_file_name, spark).withColumnRenamed('partner', 'client_id')

# plt_df = df.toPandas()
plt_df = df.filter(df.sum_monetary_w_coefficient < 3e-8).toPandas()

if sample_size is not None:
  plt_df = plt_df.sample(n = int(sample_size))

fig = plt.figure()
axs = fig.add_subplot(projection = '3d')

axs.scatter(plt_df['sum_monetary_coefficient'], plt_df['sum_monetary_w_coefficient'], plt_df['between_last_today'])
axs.set_xlabel('sum_monetary_coefficient')
axs.set_ylabel('sum_monetary_w_coefficient')
axs.set_zlabel('between_last_today')
axs.set_title('sum_monetary_coefficient / sum_monetary_w_coefficient / between_last_today')
plt.show()

# Завершаем сессию Apache Spark
spark.stop()
