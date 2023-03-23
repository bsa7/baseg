import sys
from pyspark.sql import SparkSession

if len(sys.argv) < 2:
  raise ValueError('Ошибка! Вы должны указать имя файла первым аргументом!')

file_name = sys.argv[1]

print(f'=============== Файл {file_name} ===============')

spark = SparkSession.builder.appName('ParquetInfoWithSpark').getOrCreate()
df = spark.read.parquet(file_name)
df.show(20)
spark.stop()
