import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title = "Superstore Analysis", use_pages = True)
server=app.server

sidebar = html.Div(
    children = [
        html.Div(
            children = dcc.Link(f"{page['name']}", href = page["relative_path"])
        ) for page in dash.page_registry.values()
    ],
)

app.layout = html.Div(
    children = [
        dbc.Row(
            children = [
                dbc.Col(
                    children = sidebar,
                    width = 1
                ),
                dbc.Col(
                    children = [
                        dash.page_container
                    ],
                )
            ]
        )
    ],
    className = "bg-dark"
)

if __name__ == '__main__':
    app.run_server(debug = False, use_reloader = True)