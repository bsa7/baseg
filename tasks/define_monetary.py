''' Этот файл содержит код, который по parquet-файлу с данными находит среднюю monetary для зарплатных карт '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python -m tasks.define_monetary input_file=../baseg-shared/data/wallet_urfu.parquet.gzip
import matplotlib.pyplot as plt
import pandas as pd
import pdb
import sys
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

spark = ServiceFactory().spark('Define monetary')
df = Parquet().read_to_spark_df(input_file_name, spark)

df.createOrReplaceTempView('replenishments')

def filter_sql(year):
  return f"""--beginsql
    SELECT
      AVG(average_monetary) AS average_monetary
    FROM (
      SELECT
        client_id,
        AVG(monetary_month) AS average_monetary,
        COUNT(rep_year_month) AS months_per_year,
        LEFT(rep_year_month, 4) AS rep_year
      FROM (
        SELECT
          partner AS client_id,
          COUNT(rep_date) AS replenishments_count,
          CONCAT(CAST(YEAR(rep_date) AS VARCHAR(4)), RIGHT(CONCAT('00', CAST(MONTH(rep_date) AS VARCHAR(2))), 2)) AS rep_year_month,
          SUM(monetary) AS monetary_month
        FROM replenishments
        WHERE YEAR(rep_date) = {year}
        GROUP BY
          partner,
          rep_year_month
      ) monthly_replenishments
      WHERE monthly_replenishments.replenishments_count = 2
      GROUP BY
        client_id,
        rep_year
    ) yearly_replenishments
    WHERE yearly_replenishments.months_per_year > 6
    GROUP BY
      rep_year
  --endsql"""

# По годам средняя зарплата
# 'o' - по Свердловской области по данным росстата
# 'd' - По данным запроса к датасету, предоставленному банком
average_monetary = {
  '2016': { 'year': 2016, 'average_salary': 32348, 'average_monetary': None },
  '2017': { 'year': 2017, 'average_salary': 34760, 'average_monetary': None },
  '2018': { 'year': 2018, 'average_salary': 38052, 'average_monetary': None },
  '2019': { 'year': 2019, 'average_salary': 41110, 'average_monetary': None },
  '2020': { 'year': 2020, 'average_salary': 43256, 'average_monetary': None },
  '2021': { 'year': 2021, 'average_salary': 48390, 'average_monetary': None },
  '2022': { 'year': 2022, 'average_salary': 49500, 'average_monetary': None },
}

for year in range(2016, 2023):
  sql = filter_sql(year)
  filtered_df = spark.sql(sql).toPandas()
  average_monetary[str(year)]['average_monetary'] = filtered_df['average_monetary'][0]
  print(f'=========== Year: {year} ===========')
  print(filtered_df)

average_monetary = pd.DataFrame(average_monetary.values())
average_monetary['absolute_monetary'] = average_monetary['average_monetary'] * 5.0e14
print(f'{average_monetary=}')
fig = plt.figure()
axs = fig.add_subplot()
axs.plot(average_monetary['year'], average_monetary[['average_salary', 'absolute_monetary']])
axs.set_xlabel('Год')
axs.set_ylabel('Зарплата, руб')
axs.legend(['Средняя зарплата по Свердловской области', 'monetary * 5e14'])
plt.show()

print()
print(average_monetary)
