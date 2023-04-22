# Этот скрипт выполняет кластеризацию на основе rfm датасета с колонками - client_id, r, f, m
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с rfm фичами
# Пример запуска:
# Обратите внимание, что для файлов используется папка ../data - снаружи текущего репозитория
# python -m tasks.rfm_k_means_clustering input_file=../baseg-shared/result.parquet sample_size=100000 n_clusters=4

import matplotlib.pyplot as plt
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet
from sklearn.cluster import KMeans

argument_parser = ArgumentParser()
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с rfm признаками')
sample_size = argument_parser.argument_safe('sample_size')
n_clusters = argument_parser.argument_safe('n_clusters') or '4'
print(f'=============== Обрабатывается файл {input_file_name} ===============')

spark = ServiceFactory().spark('RMF-KMeans')
df = Parquet().read_to_spark_df(input_file_name, spark)
df = df.filter(df.m < 1e-7).toPandas()

kmeans = KMeans(n_clusters = int(n_clusters))
print('--------------------------- Начали kmeans.fit --------------------------------')
df_copy = df[['r', 'f', 'm']]
print('df_copy.head()')
print(f'{df_copy.head()}')
kmeans.fit(df_copy)
print('--------------------------- Завершили kmeans.fit --------------------------------')
df['labels'] = kmeans.labels_
# print(f'{kmeans.labels_=}')
print(f'{df.shape=}')
print(f'{kmeans.labels_.shape=}')
print(df)

# new_colors = kmeans.cluster_centers_[kmeans.predict(data)]
# plot_pixels(data, colors = new_colors, title = 'Reduced color space: 16 colors')

fig = plt.figure()
axs = fig.add_subplot(projection = '3d')

if sample_size is not None:
  df = df.sample(n = int(sample_size))

axs.scatter(df['r'], df['f'], df['m'], c = df['labels'])
axs.set_xlabel('r')
axs.set_ylabel('f')
axs.set_zlabel('m')
axs.set_title('r / f / m')
plt.show()

# Завершаем сессию Apache Spark
spark.stop()
