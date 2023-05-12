''' Этот файл содержит код, который по parquet-файлу с данными пополнений для каждого клиента строит визуализацию '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python -m tasks.client_behaviour_visualization from_date=01.03.2021 finish_date=01.03.2023 input_file=../baseg-shared/data/behaviour.parquet

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import pdb
import pyarrow.parquet as pq
import time

from app.lib.argument_parser import ArgumentParser
from app.lib.utils import parse_date, timestamp_to_formatted_date

argument_parser = ArgumentParser()
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
start_date = argument_parser.argument_safe('start_date', 'Ошибка! Вы должны указать дату в формате dd.mm.yyyy, начиная с которой нужно найти признаки')
finish_date = argument_parser.argument_safe('finish_date', 'Ошибка! Вы должны указать дату в формате dd.mm.yyyy, на которую нужно найти признаки')

table = pq.read_table(input_file_name)
df = table.to_pandas()
# pdb.set_trace()

def plot(ax):
  row = df.iloc[0]
  replenishments_by_day = row['replenishments_by_day']
  days = np.array(range(0, len(replenishments_by_day)))
  return ax.plot(days, replenishments_by_day)[0]

row = df.iloc[0]
day_count = len(row['replenishments_by_day'])

fig, ax = plt.subplots(nrows=1)
ax.set_ylim(0, 200000)
ax.set_xticks(np.arange(0, day_count, 28))
ax.set_xlabel(f'Дни: с {start_date} по {finish_date}')
ax.set_ylabel('Сумма пополнения, руб.')
title = ax.text(0.1, 0.1, '', bbox={ 'facecolor':'w', 'alpha': 0.5, 'pad': 5 }, transform=ax.transAxes, ha="center")

row_count = len(df)
row = df.iloc[0]
days = np.array(range(0, len(row['replenishments_by_day'])))

line = plot(ax)
line.set_xdata(days)

def animate(i):
  row = df.iloc[i]
  client_id = row['client_id']
  replenishments_by_day = row['replenishments_by_day']
  line.set_ydata(replenishments_by_day)
  title.set_text(f'client_id: {client_id}')
  return [line]

ani = animation.FuncAnimation(fig, animate, range(1, len(df)), interval=40, blit=False)
plt.show()

