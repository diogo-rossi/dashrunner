import numpy as np
from plotly.graph_objects import Figure, Scatter, Layout
from dash import Dash
from dash.dcc import Graph
from dash.html import Div
import dashrunner as dr

app = Dash(__name__)

x = np.linspace(0, 10, 100)
y = np.sin(x)
scatter: Scatter = Scatter(x=x, y=y)
layout: Layout = Layout(template="simple_white", plot_bgcolor="white")
fig = Figure(layout=layout)
fig.add_trace(trace=scatter)

app.layout = Div([Graph(figure=fig)])
dr.run(app, screen=1, maximized=False)
