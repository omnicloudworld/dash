# pylint: disable=missing-docstring

import re
from importlib import import_module as im
from os import environ as env
from os import path
from pathlib import Path

import dash_bootstrap_components as dbc
import flask
import requests
from asgiref.wsgi import WsgiToAsgi
from dash import Dash, dcc, html
from hypercorn.middleware import AsyncioWSGIMiddleware
from jupyter_dash import JupyterDash

base_url = env.get('BASE_URL', '/')
static_path = path.join(path.dirname(path.abspath(__file__)), 'static')


class BootstrappedDash(Dash):
    '''
    Prepared a plotly dash class which includes:
    - uploaded a Bootstrap theme;
    - uploaded Google fonts: Comfortaa, Montserrat, Roboto and Material Icons;
    - setted up responsive metatag.

    Additionaly the BootstrappedDash class processed environment variables:
    - BASE_URL: leading part of the path;
    - FAVICON_URL:
    '''

    def __init__(
        self,
        name: str,
        prevent_initial_callbacks: bool = False,
        suppress_callback_exceptions: bool = True,
        default_theme: str = 'DARKLY',
        **kw
    ):

        assert re.match(r'^(\/[0-9a-z_\-\.\/]+)*\/$', base_url), 'base_url isn\'t correct'

        _themes = [
            'CERULEAN', 'COSMO', 'CYBORG', 'DARKLY', 'FLATLY', 'JOURNAL',
            'LITERA', 'LUMEN', 'LUX', 'MATERIA', 'MINTY', 'MORPH', 'PULSE',
            'QUARTZ', 'SANDSTONE', 'SIMPLEX', 'SKETCHY', 'SLATE', 'SOLAR',
            'SPACELAB', 'SUPERHERO', 'UNITED', 'VAPOR', 'YETI', 'ZEPHYR'
        ]
        assert default_theme in _themes, f'Only predefined theme is allowed. Please select from {_themes}'
        bootstrap_theme = getattr(im('dash_bootstrap_components.themes'), default_theme)

        self._name = name

        external_scripts = external_scripts = [
        ]
        self._external_scripts = self._external_scripts if hasattr(self, '_external_scripts') else []
        self._external_scripts.extend(external_scripts)
        if 'external_scripts' in kw and kw['external_scripts'] != '':
            self._external_scripts.extend(kw['external_scripts'])
            del kw['external_scripts']

        # An adding corporate styles
        external_stylesheets = [
            {
                'href': 'https://fonts.googleapis.com',
                'rel': 'preconnect'
            },
            {
                'href': 'https://fonts.gstatic.com',
                'rel': 'preconnect',
                'crossorigin': 'crossorigin'
            },
            {
                'href': ''.join([
                    'https://fonts.googleapis.com/css2?',
                    'family=Comfortaa:wght@300;400;600;700&',
                    'family=Montserrat:ital,wght@0,100;0,200;0,400;0,600;1,100;1,200;1,400;1,600&',
                    'family=Roboto:ital,wght@0,100;0,300;0,500;1,100;1,300;1,500&'
                    'display=swap'
                ]),
                'rel': 'stylesheet'
            },
            {
                'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
                'rel': 'stylesheet'
            },
            {
                'href': 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200',
                'rel': 'stylesheet'
            }
        ]
        self._external_stylesheets = self._external_stylesheets if hasattr(self, '_external_stylesheets') else []
        self._external_stylesheets.extend(external_stylesheets)
        self._external_stylesheets.extend([dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])
        self._external_stylesheets.append(bootstrap_theme)
        if 'external_stylesheets' in kw and kw['external_stylesheets'] != '':
            self._external_stylesheets.extend(kw['external_stylesheets'])
            del kw['external_stylesheets']

        meta_tags = [
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
        self._meta_tags = self._meta_tags if hasattr(self, '_meta_tags') else []
        self._meta_tags.extend(meta_tags)
        if 'meta_tags' in kw and kw['meta_tags'] != '':
            self._external_stylesheets.extend(kw['meta_tags'])
            del kw['meta_tags']

        super().__init__(
            name=re.sub(r'[ ]+', '', name.title()),
            title=name.upper(),
            compress=True,
            url_base_pathname=base_url,
            prevent_initial_callbacks=prevent_initial_callbacks,
            suppress_callback_exceptions=suppress_callback_exceptions,
            meta_tags=self._meta_tags,
            external_stylesheets=self._external_stylesheets,
            external_scripts=self._external_scripts,
            **kw
        )

        #  Make layout
        self._page = html.Section(
            id='page'
        )
        self._location = html.Div(  # for read url from dash
            [
                dcc.Location(id='url', refresh=False)
            ],
            id='location',
            style={'display': 'none'}
        )
        self.layout = html.Div(
            [
                self._location,
                self._page
            ],
            id='root'
        )

        if 'FAVICON_URL' in env and env['FAVICON_URL'] != '':
            # change default favicon
            Path('assets').mkdir(parents=True, exist_ok=True)
            img_data = requests.get(env['FAVICON_URL']).content
            with open('assets/favicon.png', 'wb') as handler:
                handler.write(img_data)
            self._favicon = 'favicon.png'

    def layouter(self, children):
        '''
        This method fill the page layout, exclude location
        '''
        self._page.children = children
        layout = html.Div(
            [
                self._location,
                self._page
            ]
        )
        self.layout = layout

    @property
    def name(self):
        '''
        Application name.
        '''

        return self._name


class SkyAntServers(Dash):
    '''
    '''

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8008,
        **kw
    ):
        super().__init__(**kw)
        self._port = port
        self._host = host

    def debug_server(
        self,
        debug: bool = True,
        **kw
    ):
        '''
        Debug server for development
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')
            def serve_static(resource):
                '''
                '''
                return flask.send_from_directory(static_path, resource)

        self.run_server(debug=debug, port=self._port, host=self._host, **kw)

    @property
    def async_server(self):
        '''
        Run service as async for working with hypercorn & http/2
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')
            def serve_static(resource):
                return flask.send_from_directory(static_path, resource)

        return AsyncioWSGIMiddleware(self.server)

    @property
    def asgi_server(self):
        '''
        Run service as async for working with asgiref package.
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')
            def serve_static(resource):
                return flask.send_from_directory(static_path, resource)

        return WsgiToAsgi(self.server)


class PyScriptDash(Dash):
    '''
    '''

    def __init__(
        self,
        prevent_initial_callbacks: bool = False,
        suppress_callback_exceptions: bool = True,
        **kw
    ):

        external_scripts = external_scripts = [
            {
                'src': 'https://pyscript.net/alpha/pyscript.js',
                'crossorigin': 'defer'
            }
        ]
        self._external_scripts = self._external_scripts if hasattr(self, '_external_scripts') else []
        self._external_scripts.extend(external_scripts)
        if 'external_scripts' in kw and kw['external_scripts'] != '':
            self._external_scripts.extend(kw['external_scripts'])

        # An adding corporate styles
        external_stylesheets = [
            {
                'href': 'https://pyscript.net/alpha/pyscript.css',
                'rel': 'stylesheet'
            },
            {
                'href': 'https://pyscript.net/alpha/pyscript.css',
                'rel': 'stylesheet'
            }
        ]
        self._external_stylesheets = self._external_stylesheets if hasattr(self, '_external_stylesheets') else []
        self._external_stylesheets.extend(external_stylesheets)
        if 'external_stylesheets' in kw and kw['external_stylesheets'] != '':
            self._external_stylesheets.extend(kw['external_stylesheets'])

        meta_tags = [
        ]
        self._meta_tags = self._meta_tags if hasattr(self, '_meta_tags') else []
        self._meta_tags.extend(meta_tags)
        if 'meta_tags' in kw and kw['meta_tags'] != '':
            self._external_stylesheets.extend(kw['meta_tags'])

        super().__init__(
            url_base_pathname=base_url,
            prevent_initial_callbacks=prevent_initial_callbacks,
            suppress_callback_exceptions=suppress_callback_exceptions,
            meta_tags=self._meta_tags,
            external_stylesheets=self._external_stylesheets,
            external_scripts=self._external_scripts,
            **kw
        )


class CoLabDash(JupyterDash):
    '''
    '''

    def __init__(
        self,
        debug: bool = True,
        host: str = '0.0.0.0',
        port: int = 8008,
        **kw
    ):
        super().__init__(**kw)
        self._debug = debug
        self._port = port
        self._host = host

    def cell(self, **kw):
        self.run_server(
            mode='inline',
            host=self._host,
            port=self._port,
            dev_tools_ui=self._debug,
            debug=self._debug,
            dev_tools_hot_reload=self._debug,
            **kw
        )

    def page(self, **kw):
        self.run_server(
            mode='jupyterlab',
            host=self._host,
            port=self._port,
            dev_tools_ui=self._debug,
            debug=self._debug,
            dev_tools_hot_reload=self._debug,
            threaded=True,
            **kw
        )
