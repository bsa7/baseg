import plotly.express as px


# Какие нужны графики:
# Скаттер 2д
# Скаттер 3д
# Боксы
# Пироги

# Разработать универсальные функции (возможно, с переменным кол-во аргументов)
# для однострочного использования
# при визуализации данных


def scat2d(df, x_col, y_col, color=None):
    fig = px.scatter(df,
                     x=x_col,
                     y=y_col,
                     color=color)
    fig.show()


def scat3d(df, x_col, y_col, z_col, color=None):
    fig = px.scatter_3d(df,
                        x=x_col,
                        y=y_col,
                        z=z_col,
                        color=color)
    fig.show()


def box():
    pass


def pie():
    pass
