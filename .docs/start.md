---
hide:
    - navigation
---


#


All SkyANT packages required the Python 3.10 or above.
You should install skyant-ui in your environment.

```bash
pip3 install --upgrade skyant-ui
```

A minimal application will be run by executing next file:
```python3 linenums='1' title='index.py'
#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped

app = Bootstrapped('Name')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8008)
```

----


## Theming

Dash application with preloaded Bootstrap

```py linenums='1' title='index.py'
#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped

app = Bootstrapped(
    'Name',
    default_theme=Bootstrapped.theme.SUPERHERO
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8008)
```

Please found more details about the class Bootstrapped [at the design page](design.md).

Definitely you can add global (corporate) CSS
```py linenums='1' title='index.py'
#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped

app = Bootstrapped(
    'Name',
    default_theme=Bootstrapped.theme.SUPERHERO, # (1)!
    external_stylesheets='https://static.example.com/some.css'
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8008)
```

1. Please found full list of themes and preview on [developer web site](https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/)



## HTTP/2

The protocol HTTP version 2.0 is a binary and multiplexing protocol for web applications. 
    [HTTP/2](https://en.wikipedia.org/wiki/HTTP/2) is more secure & faster than previous versions.

The package skyant.ui.app provides two methods with different middleware:

- async_server return hypercorn.middleware.AsyncioWSGIMiddleware
- asgi_server return asgiref.wsgi.WsgiToAsgi

```py linenums='1' title='index.py'
from skyant.ui.app import Servers

app = Servers('Name')
```

```bash
hypercorn -w 1 --bind 0.0.0.0:8008 index:app.asgi_server
```

Please fount more details on [the Servers page](serving.md).


## Serving any files

The class skyant.ui.app.Servers provides features for serving any local files that located in
    the directory 'static' near the application file.

Please fount more details on [the Servers page](serving.md).


## Jupyter/CoLab

The package [jupyter_dash](https://pypi.org/project/jupyter-dash/) provides a class for making
    an application inside a Jupyter.

In the skyant.ui.app.CoLab you would found very useful methods for run jupyter_dash in cell
    output or in separate tab.

```py linenums='1' title='make application'
from dash import html
from skyant.ui.app import CoLab

app = CoLab()
app.layout = html.Div([
    html.H1("JupyterDash Demo")
])
```

```py linenums='1' title='run in a cell output'
app.cell()
```

```py linenums='1' title='run in a separate tab'
app.page()
```

```py linenums='1' title='stop an active dash application'
app.stop_jupyter()
```


## Cloud Run (GCP)

For fast & useful deployment your application to Google Cloud Platform you can use
    [the preinstalled container](https://skyant.dev/projects/cloudrun/) from SkyANT.
