''' Этот файл содержит методы для чтения / записи parquett файлов '''

class Parquet:
  ''' Этот класс реализует методы чтения / записи датафреймов в и из parquet файлов '''
  def read_to_spark_df(self, file_name: str, spark):
    ''' Этот метод читает parquet файл в pandas датафрейм '''
    return spark.read.parquet(file_name)

  def write(self, df, file_name: str):
    ''' Этот метод пишет датафрейм в parquet файл '''
    df.to_parquet(file_name)
