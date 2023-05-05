from dash import Dash, dcc, html, Input, Output


class Dashboard:
    def __init__(self):
        self.app = Dash(__name__)
        self.graphs = []

    def add_graph(self, *figures):
        for fig in figures:
            self.graphs.append(dcc.Graph(figure=fig))

    def start(self):
        self._build_layout()
        self.app.run_server(debug=True)

    def _build_layout(self):
        graph_containers = []

        for i, graph in enumerate(self.graphs):
            graph_title = html.H2(children=f"График {i + 1}",
                                  style={"text-align": "center"})

            graph_container = html.Div(
                style={
                    #"display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "outline": "1px solid #000",
                },
                children=[graph_title, graph],
                className="graph-container",
            )
            graph_containers.append(graph_container)

        dashboard_title = html.H1(children="Дримтим дашборд", style={"text-align": "center"})

        column = html.Div(graph_containers, className="column")

        self.app.layout = html.Div(children=[dashboard_title, column],
                                   className="container")
