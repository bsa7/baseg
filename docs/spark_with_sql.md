# Использование SQL в Spark

Для выполнения SQL-запросов в Apache Spark нужно:
1. Загрузить необходимые зависимости:
  ```python
  from app.lib.service_factory import ServiceFactory
  from app.lib.parquet import Parquet
  ```
2. Создать сессию Spark:
  ```python
  spark = ServiceFactory().spark('SparkWithSQL')
  ```
3. Загрузить данные, например из паркет-файла в Spark датафрейм:
  ```python
  df = Parquet().read_to_spark_df(input_file_name, spark)
  ```
4. Создать временный View:
  ```python
  df.createOrReplaceTempView('replenishments')
  ```
5. Написать запрос:
  ```python
  query = f"""--beginsql
    SELECT
      max(rep_date) AS max_date,
      min(rep_date) AS min_date
    FROM replenishments
  --endsql"""
  ```
6. Выполнить запрос:
  ```python
  result = spark.sql(query)
  ```
7. Вывести результаты на экран:
  ```python
  result.show(10)
  ```
