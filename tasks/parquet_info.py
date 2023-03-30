''' Этот файл содержит код, который выдаёт инфу по parquet-файлу с данными '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python -m ./tasks/parquet_info.py input_file=../baseg-shared/data/wallet_urfu.parquet.gzip
import sys
import pyarrow.parquet as pq
from app.lib.argument_parser import ArgumentParser

argument_parser = ArgumentParser()

input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

table = pq.read_table(input_file_name)
schema = table.schema
print(f'{schema=}')

df = table.to_pandas()
print('=============== head ===============')
print(df.head())
print('================== tail ===================')
print(df.tail())
