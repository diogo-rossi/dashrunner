import numpy as np
from plotly.graph_objects import Figure, Scatter
import dashrunner as dr


x = np.linspace(0, 10, 100)
y = np.sin(x)
fig = Figure().add_trace(trace=Scatter(x=x, y=y))

dr.show_plotly_fig(fig, matplotlib_layout=True, debug=True, screen=1)
