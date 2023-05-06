"""
Этот скрипт содержит определения функций графиков для вывода их на dashboard
- Скаттер 2д
- Скаттер 3д
- Боксы
- Пироги
"""

import plotly.express as px


def scat2d(df, x, y, color=None):
    """
    Функция возвращает объект px.scatter

    Args:
        df (Dataframe): Датафрейм pandas
        x (str): имя столбца
        y (str): имя столбца
        color (str): имя столбца для окрашивания точек
    """
    fig = px.scatter(df, x=x, y=y, color=color, width=800, height=600)
    fig.update_traces(marker_size=2)
    return fig


def scat3d(df, x, y, z, color=None):
    """
    Функция возвращает объект px.scatter3d

    Args:
        df (Dataframe): Датафрейм pandas
        x (str): имя столбца
        y (str): имя столбца
        z (str): имя столбца
        color (str): имя столбца для окрашивания точек
    """
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=color, width=800, height=600)
    fig.update_traces(marker_size=2)
    return fig


def box(df, y, x=None, color=None, points=False):
    """
    Функция возвращает объект px.box

    Args:
        df (Dataframe): Датафрейм pandas
        y (str): имя столбца
        x (str): имя столбца (опционально)
        color (str): имя столбца для окрашивания точек
        points (str, bool) : Выводить доп. точки: points ='all',
         'outliers', 'suspectedoutliers', False
    """
    fig = px.box(df, x=x, y=y, color=color, points=points, width=800, height=600)
    fig.update_traces(quartilemethod="linear")  # or "inclusive", or "exclusive"
    return fig


def pie(df, values, names, color=None):
    """
    Функция возвращает объект px.pie

    Args:
        df (Dataframe): Датафрейм pandas
        values (str): численные значения (имя столбца)
        names (str): столбец группировки (имя столбца)
        color (str): имя столбца для окрашивания точек
    """
    fig = px.pie(df, values=values, names=names, color=color, width=800, height=600)
    return fig
