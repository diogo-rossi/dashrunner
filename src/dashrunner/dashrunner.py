from dash import Dash
from plotly.graph_objects import Figure
import webview
import os
import socket
import logging

logging.basicConfig(format="%(message)s", level=logging.INFO)

COLUMNS = os.get_terminal_size().columns

SCRIPT = r"""import os
import webview
s = ({{'screen': webview.screens[{screen}]}} if {screen} != None else {{}})
webview.create_window('{title}','http://localhost:{port}/', maximized={maximized}, **s)
webview.start()
COLUMNS = os.get_terminal_size().columns
print('-' * COLUMNS)
print('Separate script window ended. Press CTRL+C to quit Dash server in debug mode.')
print('-' * COLUMNS)
os._exit(0)"""


def get_free_port() -> int:
    """Returns the number of a free port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def run(
    app: Dash,
    port: int = 0,
    debug: bool = False,
    title: str = "My App",
    maximized: bool = True,
    screen: int | None = None,
):

    if port == 0:
        port = get_free_port()

    def run_dash():
        app.run(debug=debug, port=port, use_reloader=debug)

    if debug:

        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            import sys
            from subprocess import Popen

            python = sys.executable

            script = SCRIPT.format(
                title=title, port=port, maximized=maximized, screen=screen
            )
            command = ";".join(script.split("\n"))

            Popen(f'{python} -c "{command}"')

            logging.info("-" * COLUMNS)
            logging.info("dash runner debug mode")
            logging.info("Running the following script in a separate thread.")
            logging.info(f"Using interpreter: '{python}'")
            logging.info("```")
            logging.info(script)
            logging.info("```")
            logging.info("-" * COLUMNS)

        run_dash()

    else:
        create_window_kwargs = (
            {"screen": webview.screens[screen]} if screen is not None else {}
        )

        webview.create_window(
            title,
            f"http://localhost:{port}/",
            maximized=maximized,
            **create_window_kwargs,
        )
        webview.start(run_dash)
        os._exit(0)


def show_plotly_fig(
    figure: Figure,
    port: int = 0,
    debug: bool = False,
    title: str = "Plotly figure",
    maximized: bool = False,
    screen: int | None = None,
    matplotlib_layout: bool = False,
) -> None:
    from dash.dcc import Graph
    from dash.html import Div

    if matplotlib_layout:
        figure = (
            figure.update_layout(
                template="simple_white",
                plot_bgcolor="white",
                height=500,
                margin=dict(l=50, r=40, t=30, b=0),
            )
            .update_xaxes(mirror="allticks", ticks="inside", showgrid=True)
            .update_yaxes(mirror="allticks", ticks="inside", showgrid=True)
        )

    app = Dash(__name__)
    app.layout = Div([Graph(figure=figure)])
    run(app, port, debug, title, maximized, screen)
