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
import visual.easyplot as vis
import visual.dashboard as board

dashboard = board.Dashboard()
argument_parser = ArgumentParser()

print(f'{argument_parser.arguments=}')

input_file_name = argument_parser.argument_safe('input_file',
                                                'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
sample_size = argument_parser.argument_safe('sample_size')

print(f'=============== Обрабатывается файл {input_file_name} ===============')

spark = ServiceFactory().spark('RMFCast')
df = Parquet().read_to_spark_df(input_file_name, spark).withColumnRenamed('partner', 'client_id')

# plt_df = df.toPandas()
plt_df = df.filter(df.sum_monetary_w_coefficient < 3e-8).toPandas()

if sample_size is not None:
    plt_df = plt_df.sample(n=int(sample_size))

#Пример использования дашборда
scat3 = vis.scat3d(plt_df, 'sum_monetary_coefficient', 'sum_monetary_w_coefficient', 'between_last_today')
scat2 = vis.scat2d(plt_df, 'sum_monetary_coefficient', 'sum_monetary_w_coefficient')
box = vis.box(plt_df, 'sum_monetary_coefficient')
pie = vis.pie(plt_df[:10], 'sum_monetary_coefficient', 'client_id')
dashboard.add_graph(scat3, scat2, box, pie)
dashboard.start()

# Завершаем сессию Apache Spark
spark.stop()
