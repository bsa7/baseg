import plotly.express as px


# Какие нужны графики:
# Скаттер 2д
# Скаттер 3д
# Боксы
# Пироги

# Разработать универсальные функции (возможно, с переменным кол-во аргументов)
# для однострочного использования
# при визуализации данных


def scat2d(df, x, y, color=None, show=True):
    fig = px.scatter(df, x=x, y=y, color=color, width=800, height=600)
    fig.update_traces(marker_size=2)
    return fig


def scat3d(df, x, y, z, color=None, show=True):
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=color, width=800, height=600)
    fig.update_traces(marker_size=2)
    return fig


def box():
    pass


def pie():
    pass
