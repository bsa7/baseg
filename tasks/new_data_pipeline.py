import copy
import pandas as pd

from app.lib.argument_parser import ArgumentParser

# Запуск: 
# python -m tasks.new_features_pipeline path_in=path/to/wallet_urfu.parquet.gzip path_out=where/to/save/features.parquet.gzip req_date='mm/dd/yy'

# Пример:
# python -m tasks.new_features_pipeline path_in=s3a://some_bucket/some_dir path_out=s3a://some_bucket2/some_dir2 req_date=04/02/23

argument_parser = ArgumentParser()

path_in = argument_parser.argument_safe('path_in','Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
path_out = argument_parser.argument_safe('path_out')
date = str(argument_parser.argument_safe('req_date', 'Ошибка! Вы должны указать дату, на которую собираются фичи!'))

req_date = pd.to_datetime(date)
df = pd.read_parquet(path_in)

date_difference = copy.deepcopy(df)

date_difference["rep_date"] = (
    pd.to_datetime(date_difference["rep_date"])
    .dt.to_period('M')
    .dt.to_timestamp()
)

date_difference = (
    date_difference
        .groupby('partner', as_index=False)['rep_date']
        .agg(['first', 'last'])
        .reset_index()
)

date_difference['between_first_last'] = (
    (date_difference['last'] - date_difference['first']).dt.days
)

date_difference['between_last_today'] = (
    (req_date - date_difference['last'])
    .dt.days
)

date_difference.drop(['first', 'last'], axis=1, inplace=True)

mon_calc = copy.deepcopy(df)

mon_calc["rep_date"] = pd.to_datetime(mon_calc["rep_date"]).dt.to_period('M').dt.to_timestamp()

mon_calc['date_difference'] = (req_date - mon_calc['rep_date']).dt.days

mon_calc['monetary_coefficient'] = (1 - mon_calc['date_difference']//90 * 0.025)

mon_calc['monetary_with_coefficient'] = (mon_calc['monetary'] * mon_calc['monetary_coefficient'])

mon_calc = (
    mon_calc
        .groupby('partner')
        .agg(
          summ_monetary_w_coeff=('monetary_with_coefficient', 'sum'), 
          transactions_count_w_coeff=('monetary_coefficient', 'sum')
        )
    )

req_cols = [
                'partner', 
                'summ_monetary_w_coeff',	
                'transactions_count_w_coeff', 
                'between_first_last',	
                'between_last_today'
            ]

res = (
    mon_calc
        .join(date_difference, 'partner', 'inner')
        [req_cols]
    )

res.to_parquet(
    path_out,
    compression='gzip'
)  